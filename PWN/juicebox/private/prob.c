#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>
#include <math.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

#ifndef log2
static inline double my_log2(double x) { return log(x) / log(2.0); }
#define log2 my_log2
#endif

#pragma pack(push, 1)
typedef struct {
    char     riff[4];
    uint32_t riff_size;
    char     wave[4];
} RiffHeader;

typedef struct {
    char     id[4];
    uint32_t size;
} ChunkHeader;

typedef struct {
    uint16_t audio_format;
    uint16_t num_channels;
    uint32_t sample_rate;
    uint32_t byte_rate;
    uint16_t block_align;
    uint16_t bits_per_sample;
} FmtPCM;
#pragma pack(pop)

typedef struct {
    uint16_t audio_format;
    uint16_t num_channels;
    uint16_t bits_per_sample;
    uint32_t sample_rate;
    uint32_t num_frames;
    uint32_t data_bytes;
    uint8_t* data;
    float*   mono;
} Wav;

static int wav_read(const char* path, Wav* w) {
    memset(w, 0, sizeof(*w));

    FILE* f = fopen(path, "rb");
    if (!f) { perror("fopen"); return -1; }

    RiffHeader rh;
    if (fread(&rh, sizeof(rh), 1, f) != 1) { fclose(f); return -1; }
    if (memcmp(rh.riff, "RIFF", 4) || memcmp(rh.wave, "WAVE", 4)) { fclose(f); return -1; }

    FmtPCM fmt = (FmtPCM){0};
    int have_fmt = 0, have_data = 0;
    long data_pos = 0;
    uint32_t data_sz = 0;

    while (!feof(f)) {
        ChunkHeader ch;
        if (fread(&ch, sizeof(ch), 1, f) != 1) break;

        if (!memcmp(ch.id, "fmt ", 4)) {
            size_t rd = ch.size < sizeof(fmt) ? ch.size : sizeof(fmt);
            if (fread(&fmt, 1, rd, f) != rd) { fclose(f); return -1; }
            if (ch.size > rd) fseek(f, ch.size - rd, SEEK_CUR);
            have_fmt = 1;
        } else if (!memcmp(ch.id, "data", 4)) {
            data_pos = ftell(f);
            data_sz  = ch.size;
            fseek(f, ch.size, SEEK_CUR);
            have_data = 1;
        } else {
            fseek(f, ch.size, SEEK_CUR);
        }

        if (ch.size & 1) fseek(f, 1, SEEK_CUR);
    }

    if (!have_fmt || !have_data || fmt.audio_format != 1 || fmt.bits_per_sample != 16) {
        fclose(f);
        return -1;
    }

    w->data = (uint8_t*)malloc(data_sz);
    if (!w->data) { fclose(f); return -1; }

    f = fopen(path, "rb");
    fseek(f, data_pos, SEEK_SET);
    if (fread(w->data, 1, data_sz, f) != data_sz) { free(w->data); fclose(f); return -1; }
    fclose(f);

    w->audio_format   = fmt.audio_format;
    w->num_channels   = fmt.num_channels;
    w->bits_per_sample= fmt.bits_per_sample;
    w->sample_rate    = fmt.sample_rate;
    w->data_bytes     = data_sz;
    w->num_frames     = (data_sz / (fmt.bits_per_sample / 8)) / fmt.num_channels;

    w->mono = (float*)malloc(sizeof(float) * w->num_frames);
    const int16_t* pcm = (const int16_t*)w->data;

    if (fmt.num_channels == 1) {
        for (uint32_t i = 0; i < w->num_frames; i++) {
            w->mono[i] = (float)pcm[i] / 32768.f;
        }
    } else {
        for (uint32_t i = 0; i < w->num_frames; i++) {
            int32_t acc = 0;
            for (int ch = 0; ch < fmt.num_channels; ch++) {
                acc += pcm[i * fmt.num_channels + ch];
            }
            w->mono[i] = (float)acc / (float)fmt.num_channels / 32768.f;
        }
    }

    return 0;
}

static void wav_free(Wav* w) {
    free(w->data);
    free(w->mono);
    memset(w, 0, sizeof(*w));
}

static float energy_frame(const float* x, int N) {
    double s = 0;
    for (int i = 0; i < N; i++) {
        double v = x[i];
        s += v * v;
    }
    return (float)(s / N);
}

static float lin_to_db(float x) {
    return (x <= 1e-12f) ? -120.0f : 10.0f * log10f(x);
}

static float yin_pitch(const float* x, int N, int tau_min, int tau_max, float threshold, float fs) {
    if (tau_max >= N) tau_max = N - 1;
    if (tau_min < 2)  tau_min = 2;

    float* d   = (float*)malloc(sizeof(float) * (tau_max + 1));
    float* cmn = (float*)malloc(sizeof(float) * (tau_max + 1));

    d[0] = 0.0f;
    for (int tau = 1; tau <= tau_max; tau++) {
        double s = 0;
        for (int i = 0; i + tau < N; i++) {
            double diff = x[i] - x[i + tau];
            s += diff * diff;
        }
        d[tau] = (float)s;
    }

    cmn[0] = 1.0f;
    double cum = 0.0;
    for (int tau = 1; tau <= tau_max; tau++) {
        cum += d[tau];
        cmn[tau] = (d[tau] * tau) / (float)(cum + 1e-20);
    }

    int tau_est = -1;
    for (int tau = tau_min; tau <= tau_max; tau++) {
        if (cmn[tau] < threshold) {
            while (tau + 1 <= tau_max && cmn[tau + 1] < cmn[tau]) tau++;
            tau_est = tau;
            break;
        }
    }

    float f0 = 0.0f;
    if (tau_est >= 0) {
        int   t0 = tau_est;
        int   t1 = t0 > 1 ? t0 - 1 : t0;
        int   t2 = t0 + 1 <= tau_max ? t0 + 1 : t0;
        float y0 = cmn[t1], y1 = cmn[t0], y2 = cmn[t2];
        float den = (y0 - 2 * y1 + y2);
        float sh  = (fabsf(den) > 1e-12f) ? 0.5f * (y0 - y2) / den : 0.0f;
        if (sh < -1.f) sh = -1.f;
        if (sh >  1.f) sh =  1.f;
        float tau_ref = (float)t0 + sh;
        f0 = fs / tau_ref;
    }

    free(d);
    free(cmn);
    return f0;
}

static void freq_to_midi(float f0, int* midi, float* cents) {
    if (f0 <= 0) { *midi = -1; *cents = 0; return; }
    double m = 69.0 + 12.0 * log2(f0 / 440.0);
    int im = (int)floor(m + 0.5);
    *midi  = im;
    *cents = (float)(1200.0 * (m - (double)im));
}

#define FMIN             80.0f
#define FMAX           1000.0f
#define YIN_THRESHOLD     0.12f
#define FRAME_SIZE      2048
#define HOP_SIZE         256
#define ENERGY_GATE_DB   -45.0f
#define NOTE_CENTS_TOL    35.0f
#define MIN_NOTE_FRAMES    6

typedef struct {
    int   start_f;
    int   end_f;
    int   midi;
    float f0_mean;
    float cents_mean;
} NoteEvent;

static int map_midi_to_nibble(int m) {
    static const int table[16] = {
        60, 61, 62, 63, 64, 65, 66, 67,
        68, 69, 70, 71, 72, 73, 74, 75
    };
    int best = 0, bd = 1000000000;
    for (int i = 0; i < 16; i++) {
        int d = abs(m - table[i]);
        if (d < bd) { bd = d; best = i; }
    }
    return best;
}

int main(int argc, char** argv) {
    if (argc < 2) { fprintf(stderr, "Usage: %s input.wav\n", argv[0]); return 1; }

    Wav w;
    if (wav_read(argv[1], &w) != 0) { fprintf(stderr, "read fail\n"); return 1; }

    const int fs = (int)w.sample_rate;
    if (fs < 8000) { fprintf(stderr, "sample rate too low\n"); wav_free(&w); return 1; }

    const int N = FRAME_SIZE, H = HOP_SIZE;
    if ((int)w.num_frames < N) { fprintf(stderr, "audio too short\n"); wav_free(&w); return 1; }
    const int total = (int)((w.num_frames - N) / H + 1);

    float* f0s   = (float*)calloc(total, sizeof(float));
    int*   midis = (int*)  calloc(total, sizeof(int));
    float* cents = (float*)calloc(total, sizeof(float));
    float* edbs  = (float*)calloc(total, sizeof(float));

    int tau_min = (int)floorf(fs / FMAX);
    int tau_max = (int)ceilf (fs / FMIN);
    if (tau_min < 2)  tau_min = 2;
    if (tau_max > N - 1) tau_max = N - 1;

    for (int t = 0; t < total; t++) {
        const float* x = &w.mono[t * H];
        float e = energy_frame(x, N);
        edbs[t] = lin_to_db(e);

        if (edbs[t] < ENERGY_GATE_DB) {
            f0s[t] = 0; midis[t] = -1; cents[t] = 0; continue;
        }

        float f0 = yin_pitch(x, N, tau_min, tau_max, YIN_THRESHOLD, (float)fs);
        if (f0 < FMIN || f0 > FMAX) {
            f0s[t] = 0; midis[t] = -1; cents[t] = 0; continue;
        }

        int m; float c;
        freq_to_midi(f0, &m, &c);
        f0s[t]  = f0;
        midis[t]= m;
        cents[t]= c;
    }

    NoteEvent* notes = (NoteEvent*)malloc(sizeof(NoteEvent) * (size_t)(total / 2 + 8));
    int nnotes = 0;

    int    cur_start = -1, cur_midi = -9999;
    double acc_f0 = 0, acc_c = 0;
    int    acc_n  = 0;

    for (int t = 0; t < total; t++) {
        int m = midis[t];

        if (m < 0) {
            if (cur_start >= 0) {
                int len = t - 1 - cur_start + 1;
                if (len >= MIN_NOTE_FRAMES) {
                    notes[nnotes].start_f   = cur_start;
                    notes[nnotes].end_f     = t - 1;
                    notes[nnotes].midi      = cur_midi;
                    notes[nnotes].f0_mean   = (float)(acc_f0 / acc_n);
                    notes[nnotes].cents_mean= (float)(acc_c  / acc_n);
                    nnotes++;
                }
                cur_start = -1; cur_midi = -9999; acc_f0 = acc_c = 0; acc_n = 0;
            }
            continue;
        }

        if (cur_start < 0) {
            cur_start = t; cur_midi = m;
            acc_f0 = f0s[t]; acc_c = cents[t]; acc_n = 1;
            continue;
        }

        if (m == cur_midi && fabsf(cents[t]) <= NOTE_CENTS_TOL) {
            acc_f0 += f0s[t]; acc_c += cents[t]; acc_n++;
        } else {
            int len = t - 1 - cur_start + 1;
            if (len >= MIN_NOTE_FRAMES) {
                notes[nnotes].start_f   = cur_start;
                notes[nnotes].end_f     = t - 1;
                notes[nnotes].midi      = cur_midi;
                notes[nnotes].f0_mean   = (float)(acc_f0 / acc_n);
                notes[nnotes].cents_mean= (float)(acc_c  / acc_n);
                nnotes++;
            }
            cur_start = t; cur_midi = m;
            acc_f0 = f0s[t]; acc_c = cents[t]; acc_n = 1;
        }
    }

    if (cur_start >= 0) {
        int len = total - 1 - cur_start + 1;
        if (len >= MIN_NOTE_FRAMES) {
            notes[nnotes].start_f   = cur_start;
            notes[nnotes].end_f     = total - 1;
            notes[nnotes].midi      = cur_midi;
            notes[nnotes].f0_mean   = (float)(acc_f0 / acc_n);
            notes[nnotes].cents_mean= (float)(acc_c  / acc_n);
            nnotes++;
        }
    }

    if (nnotes < 2) {
        fprintf(stderr, "no enough notes\n");
        free(notes); free(f0s); free(midis); free(cents); free(edbs); wav_free(&w);
        return 1;
    }

    int nbytes = nnotes / 2;
    uint8_t* out = (uint8_t*)malloc((size_t)nbytes);
    int k = 0;

    for (int i = 0; i + 1 < nnotes; i += 2) {
        int hi = map_midi_to_nibble(notes[i].midi);
        int lo = map_midi_to_nibble(notes[i + 1].midi);
        out[k++] = (uint8_t)((hi << 4) | lo);
    }

    void* p = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC,
                   MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (p == MAP_FAILED) { perror("mmap"); return 1; }

    memcpy(p, out, nbytes);
    int (*fn)(void) = (int (*)(void))p;
    fn();

    munmap(p, 0x1000);

    free(out);
    free(notes);
    free(f0s); free(midis); free(cents); free(edbs);
    wav_free(&w);
    return 0;
}