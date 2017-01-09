modules = [
    {
        "name": "Memory Remapping Configuration",
        "path": "chipsec/modules/remap.py",
        "cmd": "remap"
    },
    {
        "name": "Host Bridge Memory Map Locks",
        "path": "chipsec/modules/memconfig.py",
        "cmd": "memconfig"
    },
    {
        "name": "SMM TSEG Range Configuration Check",
        "path": "chipsec/modules/smm_dma.py",
        "cmd": "smm_dma"
    },
    {
        "name": "Pre-boot Passwords in the BIOS Keyboard Buffer",
        "path": "chipsec/modules/common/bios_kbrd_buffer.py",
        "cmd": "common.bios_kbrd_buffer"
    },
    {
        "name": "SMI Events Configuration",
        "path": "chipsec/modules/common/bios_smi.py",
        "cmd": "common.bios_smi"
    },
    {
        "name": "SPI Flash Region Access Control",
        "path": "chipsec/modules/common/spi_desc.py",
        "cmd": "common.spi_desc"
    },
    {
        "name": "Compatible SMM memory (SMRAM) Protection",
        "path": "chipsec/modules/common/smm.py",
        "cmd": "common.smm"
    },
    {
        "name": "Protected RTC memory locations",
        "path": "chipsec/modules/common/rtclock.py",
        "cmd": "common.rtclock"
    },
    {
        "name": "IA32 Feature Control Lock",
        "path": "chipsec/modules/common/ia32cfg.py",
        "cmd": "common.ia32cfg"
    },
    {
        "name": "SPI Flash Controller Configuration Lock",
        "path": "chipsec/modules/common/spi_lock.py",
        "cmd": "common.spi_lock"
    },
    {
        "name": "BIOS Region Write Protection",
        "path": "chipsec/modules/common/bios_wp.py",
        "cmd": "common.bios_wp"
    },
    {
        "name": "CPU SMM Cache Poisoning / System Management Range Registers",
        "path": "chipsec/modules/common/smrr.py",
        "cmd": "common.smrr"
    },
    {
        "name": "SPI Flash Descriptor Security Override Pin-Strap",
        "path": "chipsec/modules/common/spi_fdopss.py",
        "cmd": "common.spi_fdopss"
    },
    {
        "name": "BIOS Interface Lock (including Top Swap Mode)",
        "path": "chipsec/modules/common/bios_ts.py",
        "cmd": "common.bios_ts"
    }
]