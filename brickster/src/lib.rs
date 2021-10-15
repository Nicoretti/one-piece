use std::collections::hash_map::HashMap;

/// Builder used to build environment variable(s) environment.
#[derive(Debug)]
pub struct EnvBuilder {
    env: HashMap<String, String>,
}

impl EnvBuilder {
    /// Create a new `EnvBuilder`.
    ///
    /// ```rust
    /// use brickster::EnvBuilder;
    /// let builder = EnvBuilder::new();
    /// ```
    pub fn new() -> Self {
        Self {
            env: HashMap::new(),
        }
    }

    /// Clone the current system environment variables into the `EnvBuilder`.
    ///
    /// ```rust
    /// use brickster::EnvBuilder;
    /// let builder = EnvBuilder::new().clone();
    /// ```
    pub fn clone(mut self) -> Self {
        std::env::vars().for_each(|(key, value)| {
            self.env.insert(key, value);
        });
        self
    }

    /// Add an environment variable to the `EnvBuilder`.
    ///
    /// ```rust
    /// use brickster::EnvBuilder;
    /// let builder = EnvBuilder::new().add("MY_VAR", "VALUE");
    /// ```
    pub fn add(mut self, key: &str, value: &str) -> Self {
        self.env.insert(key.into(), value.into());
        self
    }

    /// Remove an environment variable from the `EnvBuilder`.
    ///
    /// ```rust
    /// use brickster::EnvBuilder;
    /// let builder = EnvBuilder::new().remove("HOME");
    /// ```
    pub fn remove(mut self, key: &str) -> Self {
        self.env.remove(key);
        self
    }

    /// Clear all environment variable from the `EnvBuilder`.
    ///
    /// ```rust
    /// use brickster::EnvBuilder;
    /// let builder = EnvBuilder::new().clone().clear();
    /// ```
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
        let builder = EnvBuilder::new().clone();
        assert_eq!(
            std::env::vars().collect::<HashMap<String, String>>(),
            builder.into()
        );
    }

    #[test]
    fn test_env_builder_add() {
        let mut expected = std::env::vars().collect::<HashMap<String, String>>();
        expected.insert(String::from("MY_TEST_VAR_XYZ"), String::from("MY_VALUE"));
        let builder = EnvBuilder::new().clone().add("MY_TEST_VAR_XYZ", "MY_VALUE");
        assert_eq!(expected, builder.into());
    }

    #[test]
    fn test_env_builder_remove() {
        let mut expected = std::env::vars().collect::<HashMap<String, String>>();
        expected.remove("HOME");
        let builder = EnvBuilder::new().clone().remove("HOME");
        assert_eq!(expected, builder.into());
    }

    #[test]
    fn test_env_builder_clear() {
        let expected: HashMap<String, String> = HashMap::new();
        let builder = EnvBuilder::new().clone().clear();
        assert_eq!(expected, builder.into());
    }
}
