use std::collections::hash_map::HashMap;

/// Builder used to build environment variable(s) environment.
#[derive(Debug)]
pub struct EnvBuilder {
    env: HashMap<String, String>,
}

impl EnvBuilder {
    /// Create a new `EnvBuilder`.
    pub fn new() -> Self {
        Self {
            env: HashMap::new(),
        }
    }

    pub fn configure<F>(self, closure: F) -> Self
    where
        F: FnOnce(Self) -> Self,
    {
        closure(self)
    }

    /// Clone the current system environment variables into the `EnvBuilder`.
    pub fn clone(mut self) -> Self {
        std::env::vars().for_each(|(key, value)| {
            self.env.insert(key, value);
        });
        self
    }

    /// Add an environment variable to the `EnvBuilder`.
    pub fn add(mut self, key: &str, value: &str) -> Self {
        self.env.insert(key.into(), value.into());
        self
    }

    /// Remove an environment variable from the `EnvBuilder`.
    pub fn remove(mut self, key: &str) -> Self {
        self.env.remove(key);
        self
    }

    /// Clear all environment variable from the `EnvBuilder`.
    pub fn clear(mut self) -> Self {
        self.env.clear();
        self
    }
}

impl Into<HashMap<String, String>> for EnvBuilder {
    fn into(self) -> HashMap<String, String> {
        self.env
    }
}

#[cfg(test)]
mod tests {
    use crate::EnvBuilder;
    use std::collections::HashMap;

    #[test]
    fn test_env_builder_clone() {
        let expected = std::env::vars();
        let mut builder = EnvBuilder::new().clone();
        assert_eq!(
            std::env::vars().collect::<HashMap<String, String>>(),
            builder.into()
        );
    }

    #[test]
    fn test_env_builder_add() {
        let mut expected = std::env::vars().collect::<HashMap<String, String>>();
        expected.insert(String::from("MY_TEST_VAR_XYZ"), String::from("MY_VALUE"));
        let mut builder = EnvBuilder::new().clone().add("MY_TEST_VAR_XYZ", "MY_VALUE");
        assert_eq!(expected, builder.into());
    }

    #[test]
    fn test_env_builder_remove() {
        let mut expected = std::env::vars().collect::<HashMap<String, String>>();
        expected.remove("HOME");
        let mut builder = EnvBuilder::new().clone().remove("HOME");
        assert_eq!(expected, builder.into());
    }

    #[test]
    fn test_env_builder_clear() {
        let expected: HashMap<String, String> = HashMap::new();
        let mut builder = EnvBuilder::new().clone().clear();
        assert_eq!(expected, builder.into());
    }

    #[test]
    fn test_env_builder_configure() {
        let mut expected: HashMap<String, String> = HashMap::new();
        expected.insert("FOO".into(), "BAR".into());
        expected.insert("BAR".into(), "FOO".into());
        expected.insert("MAM".into(), "??".into());
        let e = super::EnvBuilder::new().configure(|env| {
            env.clone()
                .clear()
                .add("FOO", "BAR")
                .add("BAR", "FOO")
                .add("MAM", "??")
        });
        assert_eq!(expected, e.into());
    }
}
