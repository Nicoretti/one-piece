use core::convert::Into;
use core::marker::PhantomData;
use core::ptr;

/// Marker trait types capable of representing a register
pub trait RegisterType {}
pub trait ValueType {}

impl RegisterType for u8 {}
impl RegisterType for u16 {}
impl RegisterType for u32 {}
impl RegisterType for u64 {}
impl RegisterType for usize {}

pub trait Read<T: RegisterType> {
    fn read(&self) -> T;
}

pub trait Write<T: RegisterType> {
    fn write(&mut self, value: T);
}

pub struct Register<T: RegisterType> {
    address: usize,
    register_type: PhantomData<T>,
}

struct TypedRegister<T: RegisterType, V: Into<T>> {
    reg: Register<T>,
    register_type: PhantomData<V>,
}

impl<T: RegisterType, V: Into<T>> TypedRegister<T, V> {
    #[inline(always)]
    fn write(&mut self, value: V) {
        self.reg.write(value.into());
    }

    #[inline(always)]
    fn read(&self) -> T {
        self.reg.read()
    }
}

impl<T: RegisterType> Register<T> {
    #[inline(always)]
    pub fn new(address: usize) -> Self {
        Register {
            address,
            register_type: PhantomData,
        }
    }
}

impl<T: RegisterType> Read<T> for Register<T> {
    #[inline(always)]
    fn read(&self) -> T {
        unsafe { ptr::read_volatile(self.address as *const T) }
    }
}

impl<T: RegisterType> Write<T> for Register<T> {
    #[inline(always)]
    fn write(&mut self, value: T) {
        unsafe { ptr::write_volatile(self.address as *mut T, value) };
    }
}

pub struct ReadOnlyRegister<T: RegisterType> {
    register: Register<T>,
}

impl<T: RegisterType> ReadOnlyRegister<T> {
    #[inline(always)]
    pub fn new(address: usize) -> Self {
        ReadOnlyRegister {
            register: Register::new(address),
        }
    }
}

impl<T: RegisterType> Read<T> for ReadOnlyRegister<T> {
    #[inline(always)]
    fn read(&self) -> T {
        self.register.read()
    }
}

pub struct WriteOnlyRegister<T: RegisterType> {
    register: Register<T>,
}

impl<T: RegisterType> WriteOnlyRegister<T> {
    #[inline(always)]
    pub fn new(address: usize) -> Self {
        WriteOnlyRegister {
            register: Register::new(address),
        }
    }
}

impl<T: RegisterType> Write<T> for WriteOnlyRegister<T> {
    #[inline(always)]
    fn write(&mut self, value: T) {
        self.register.write(value)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    // TODO: consider rewriting test based on Register type
    #[test]
    fn u8_memory_mapped_io_register_read() {
        let mut memory_mapped_io_register: u8 = 0;
        let address = (&memory_mapped_io_register as *const u8) as usize;
        let reg: Register<u8> = Register::new(address);

        assert_eq!(reg.read(), 0);
        memory_mapped_io_register = 0xFF;
        assert_eq!(reg.read(), 0xFF);
        // Dummy assert to read the variable to get rid of a warning
        assert_eq!(memory_mapped_io_register, 0xFF);
    }

    #[test]
    fn u8_memory_mapped_io_register_write() {
        let memory_mapped_io_register: u8 = 0;
        let address = (&memory_mapped_io_register as *const u8) as usize;
        let mut reg: Register<u8> = Register::new(address);

        assert_eq!(memory_mapped_io_register, 0);
        reg.write(0xFF);
        assert_eq!(memory_mapped_io_register, 0xFF);
    }

    #[test]
    fn u16_memory_mapped_io_register_read() {
        let mut memory_mapped_io_register: u16 = 0;
        let address = (&memory_mapped_io_register as *const u16) as usize;
        let reg: Register<u16> = Register::new(address);

        assert_eq!(reg.read(), 0);
        memory_mapped_io_register = 0xFFFF;
        assert_eq!(reg.read(), 0xFFFF);
        // Dummy assert to read the variable to get rid of a warning
        assert_eq!(memory_mapped_io_register, 0xFFFF);
    }

    #[test]
    fn u16_memory_mapped_io_register_write() {
        let memory_mapped_io_register: u16 = 0;
        let address = (&memory_mapped_io_register as *const u16) as usize;
        let mut reg: Register<u16> = Register::new(address);

        assert_eq!(memory_mapped_io_register, 0);
        reg.write(0xFFFF);
        assert_eq!(memory_mapped_io_register, 0xFFFF);
    }

    #[test]
    fn u32_memory_mapped_io_register_read() {
        let mut memory_mapped_io_register: u32 = 0;
        let address = (&memory_mapped_io_register as *const u32) as usize;
        let reg: Register<u32> = Register::new(address);

        assert_eq!(reg.read(), 0);
        memory_mapped_io_register = 0xFFFFFFFF;
        assert_eq!(reg.read(), 0xFFFFFFFF);
        // Dummy assert to read the variable to get rid of a warning
        assert_eq!(memory_mapped_io_register, 0xFFFFFFFF);
    }

    #[test]
    fn u32_memory_mapped_io_register_write() {
        let memory_mapped_io_register: u32 = 0;
        let address = (&memory_mapped_io_register as *const u32) as usize;
        let mut reg: Register<u32> = Register::new(address);

        assert_eq!(memory_mapped_io_register, 0);
        reg.write(0xFFFFFFFF);
        assert_eq!(memory_mapped_io_register, 0xFFFFFFFF);
    }

    #[test]
    fn u8_read_only_register() {
        let mut memory_mapped_io_register: u8 = 0;
        let address = (&memory_mapped_io_register as *const u8) as usize;
        let reg: ReadOnlyRegister<u8> = ReadOnlyRegister::new(address);

        assert_eq!(reg.read(), 0);
        memory_mapped_io_register = 0xFF;
        assert_eq!(reg.read(), 0xFF);
        // Dummy assert to read the variable to get rid of a warning
        assert_eq!(memory_mapped_io_register, 0xFF);
    }

    #[test]
    fn u16_read_only_register() {
        let mut memory_mapped_io_register: u16 = 0;
        let address = (&memory_mapped_io_register as *const u16) as usize;
        let reg: ReadOnlyRegister<u16> = ReadOnlyRegister::new(address);

        assert_eq!(reg.read(), 0);
        memory_mapped_io_register = 0xFFFF;
        assert_eq!(reg.read(), 0xFFFF);
        // Dummy assert to read the variable to get rid of a warning
        assert_eq!(memory_mapped_io_register, 0xFFFF);
    }

    #[test]
    fn u32_read_only_register() {
        let mut memory_mapped_io_register: u32 = 0;
        let address = (&memory_mapped_io_register as *const u32) as usize;
        let reg: ReadOnlyRegister<u32> = ReadOnlyRegister::new(address);

        assert_eq!(reg.read(), 0);
        memory_mapped_io_register = 0xFFFFFFFF;
        assert_eq!(reg.read(), 0xFFFFFFFF);
        // Dummy assert to read the variable to get rid of a warning
        assert_eq!(memory_mapped_io_register, 0xFFFFFFFF);
    }

    #[test]
    fn u8_write_only_register() {
        let memory_mapped_io_register: u8 = 0;
        let address = (&memory_mapped_io_register as *const u8) as usize;
        let mut reg: WriteOnlyRegister<u8> = WriteOnlyRegister::new(address);

        assert_eq!(memory_mapped_io_register, 0);
        reg.write(0xFF);
        assert_eq!(memory_mapped_io_register, 0xFF);
    }

    #[test]
    fn u16_write_only_register() {
        let memory_mapped_io_register: u16 = 0;
        let address = (&memory_mapped_io_register as *const u16) as usize;
        let mut reg: WriteOnlyRegister<u16> = WriteOnlyRegister::new(address);

        assert_eq!(memory_mapped_io_register, 0);
        reg.write(0xFFFF);
        assert_eq!(memory_mapped_io_register, 0xFFFF);
    }

    #[test]
    fn u32_write_only_register() {
        let memory_mapped_io_register: u32 = 0;
        let address = (&memory_mapped_io_register as *const u32) as usize;
        let mut reg: WriteOnlyRegister<u32> = WriteOnlyRegister::new(address);

        assert_eq!(memory_mapped_io_register, 0);
        reg.write(0xFFFFFFFF);
        assert_eq!(memory_mapped_io_register, 0xFFFFFFFF);
    }
}
