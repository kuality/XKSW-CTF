#include <linux/module.h>
#include <linux/fs.h>
#include <linux/device.h>
#include <linux/cdev.h>
#include <linux/uaccess.h>
#include <linux/slab.h>
#include <linux/ioctl.h>
#include <linux/miscdevice.h>
#include <linux/mutex.h>

#define NOTE_DEVICE_NAME "note"
#define MANAGEMENT_MAX_CHUNKS 5
#define NOTE_MAX_CHUNKS 16
#define DATA_SIZE 0x40

#define MANAGEMENT_ALLOC 0x1001
#define NOTE_ALLOC 0x1002
#define NOTE_WRITE 0x1003
#define NOTE_READ 0x1004
#define MANAGEMENT_DELETE 0x1005
#define NOTE_DELETE 0x1006

static DEFINE_MUTEX(module_lock);

typedef struct note_ioctl_data {
    unsigned long long menagement_index;
    unsigned long long note_idx;
    char payload[DATA_SIZE];
} note_ioctl_data;

typedef struct chunk_t {
    void * note[NOTE_MAX_CHUNKS];
} chunk_t;


static long note_ioctl(struct file *file, unsigned int cmd, unsigned long arg);

static chunk_t * management_chunks[MANAGEMENT_MAX_CHUNKS] = {0, };

static long note_ioctl(struct file *file, unsigned int cmd, unsigned long arg) {
    note_ioctl_data data;
    volatile int alloc_size = sizeof(chunk_t);
    memset(&data, 0, sizeof(note_ioctl_data));

    if ( copy_from_user(&data, (struct note_ioctl_data * )arg, sizeof(struct note_ioctl_data)) ){
        return -EINVAL;
    }

    mutex_lock(&module_lock);
    switch (cmd) {
        case MANAGEMENT_ALLOC:
            if (data.menagement_index >= MANAGEMENT_MAX_CHUNKS){
                return -EINVAL;
            }
            management_chunks[data.menagement_index] = (chunk_t*)kmalloc(alloc_size, GFP_KERNEL_ACCOUNT);
            if (!management_chunks[data.menagement_index]){
                return -ENOMEM;
            }
            memset(management_chunks[data.menagement_index], 0, sizeof(chunk_t));
            break;
        case NOTE_ALLOC:
            if (data.menagement_index >= MANAGEMENT_MAX_CHUNKS || data.note_idx >= NOTE_MAX_CHUNKS || !management_chunks[data.menagement_index]){
                return -EINVAL;
            }
            management_chunks[data.menagement_index]->note[data.note_idx] = kmalloc(0x40, GFP_KERNEL_ACCOUNT);
            if (!management_chunks[data.menagement_index]->note[data.note_idx]){
                return -ENOMEM;
            }
            memset(management_chunks[data.menagement_index]->note[data.note_idx], 0, 0x40);
            break;


        case NOTE_WRITE:
            if (data.menagement_index >= MANAGEMENT_MAX_CHUNKS || !management_chunks[data.menagement_index] || data.note_idx >= NOTE_MAX_CHUNKS || !management_chunks[data.menagement_index]->note[data.note_idx]){
                return -EINVAL;
            }
            memcpy(management_chunks[data.menagement_index]->note[data.note_idx], data.payload, 0x40);
            break;
        
        case NOTE_READ:
            if (data.menagement_index >= MANAGEMENT_MAX_CHUNKS || !management_chunks[data.menagement_index] || data.note_idx >= NOTE_MAX_CHUNKS || !management_chunks[data.menagement_index]->note[data.note_idx]){
                return -EINVAL;
            }
            copy_to_user(((struct note_ioctl_data *)arg)->payload, management_chunks[data.menagement_index]->note[data.note_idx], 0x40);
            break;
       

        case MANAGEMENT_DELETE:
            if (data.menagement_index >= MANAGEMENT_MAX_CHUNKS || !management_chunks[data.menagement_index]){
                return -EINVAL;
            }
            kfree(management_chunks[data.menagement_index]);
            break;


        case NOTE_DELETE:
            if (data.menagement_index >= MANAGEMENT_MAX_CHUNKS || !management_chunks[data.menagement_index] || data.note_idx >= NOTE_MAX_CHUNKS || !management_chunks[data.menagement_index]->note[data.note_idx]){
                return -EINVAL;
            }

            kfree(management_chunks[data.menagement_index]->note[data.note_idx]);
            management_chunks[data.menagement_index]->note[data.note_idx] = NULL;
            break;


        default:
            return -ENOTTY;
    }
    mutex_unlock(&module_lock);
    return 0;
}

static struct file_operations note_fops = {
    .owner = THIS_MODULE,
    .unlocked_ioctl = note_ioctl,
};

static struct miscdevice note_dev = {
    .minor = MISC_DYNAMIC_MINOR,
    .name = "note",
    .fops = &note_fops
};

static int __init note_init(void) {
    if (misc_register(&note_dev) != 0) {
        return -1;
    }
    return 0;
}

static void __exit note_exit(void) {
    misc_deregister(&note_dev);
    mutex_destroy(&module_lock);
}

module_init(note_init);
module_exit(note_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("r0jin");

