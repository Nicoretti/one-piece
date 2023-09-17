mod context {

    pub trait ContextManager {
        fn enter(self);
    }

    pub struct Context<T> {
        inner: T,
    }

    impl<T: ContextManager> Context<T> {
        pub fn enter<F>(self, closure: F)
        where
            F: FnOnce(T),
        {
            println!("Enter");
            closure(self.inner);
            drop(self);
            println!("Exit");
        }
    }

    impl<T> Drop for Context<T> {
        fn drop(&mut self) {
            todo!()
        }
    }

    impl<T: ContextManager> Context<T> {
        pub fn new(inner: T) -> Self {
            Self { inner }
        }
    }

    pub struct Environment {}

    impl Environment {
        pub fn add(self) -> Self {
            self
        }
    }

    impl ContextManager for Environment {
        fn enter(self) {
            println!("Doing Environment stuff");
        }
    }

    impl Drop for Environment {
        fn drop(&mut self) {
            println!("DROPPING ENV");
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::context;
    use crate::context::Context;
    use crate::context::ContextManager;
    use crate::context::Environment;

    #[test]
    fn it_works() {
        Context::<Environment>::new(Environment {}.add().add()).enter(|env| {
            println!("executing code");
        })
    }
}
