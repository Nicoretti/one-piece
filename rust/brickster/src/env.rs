//! structures and functionalities associated with environment variables.
use std::collections::hash_map::HashMap;
use std::ops::{Index, IndexMut};

/// Builder used to build environment variable(s) environment.
#[derive(Debug)]
pub struct EnvBuilder {
    env: HashMap<String, String>,
    empty: String,
}

impl EnvBuilder {
    /// Create a new `EnvBuilder`.
    pub fn new() -> Self {
        Self {
            env: HashMap::new(),
            empty: String::from(""),
        }
    }

    /// Configure the environment variables
    ///
    /// Example:
    /// ```rust
    /// use std::collections::hash_map::HashMap;
    /// use brickster::env::EnvBuilder;
    /// let mut expected: HashMap<String, String> = HashMap::new();
    /// expected.extend(vec![
    ///     ("FOO".into(), "BAR".into()),
    ///     ("BAR".into(), "FOO".into()),
    ///     ("MAM".into(), "??".into())
    ///  ].into_iter()
    /// );
    /// let e = EnvBuilder::new().configure(|env| {
    ///     env.clone();
    ///     env.clear();
    ///     env.add("FOO", "BAR");
    ///     env.add("BAR", "FOO");
    ///     env.add("MAM", "??");
    /// });
    /// assert_eq!(expected, e.into());
    /// ```
    pub fn configure<F>(mut self, mut closure: F) -> Self
    where
        F: FnMut(&mut Self),
    {
        closure(&mut self);
        self
    }

    /// Clone the current system environment variables into the `EnvBuilder`.
    pub fn clone(&mut self) {
        std::env::vars().for_each(|(key, value)| {
            self.env.insert(key, value);
        });
    }

    /// Add an environment variable to the `EnvBuilder`.
    pub fn add(&mut self, key: &str, value: &str) {
        self.env.insert(key.into(), value.into());
    }

    /// Remove an environment variable from the `EnvBuilder`.
    pub fn remove(&mut self, key: &str) {
        self.env.remove(key);
    }

    /// Clear all environment variable from the `EnvBuilder`.
    pub fn clear(&mut self) {
        self.env.clear();
    }
}

impl Index<&str> for EnvBuilder {
    type Output = String;

    fn index(&self, index: &str) -> &Self::Output {
        match self.env.get(index) {
            Some(v) => v,
            None => &self.empty,
        }
    }
}

impl IndexMut<&str> for EnvBuilder {
    fn index_mut(&mut self, index: &str) -> &mut Self::Output {
        match self.env.get(index) {
            Some(_) => self.env.get_mut(index).unwrap(),
            None => {
                self.env.insert(index.into(), "".into());
                self.env.get_mut(index).unwrap()
            }
        }
    }
}

impl Into<HashMap<String, String>> for EnvBuilder {
    fn into(self) -> HashMap<String, String> {
        self.env
    }
}

#[cfg(test)]
mod tests {
    use super::EnvBuilder;
    use std::collections::HashMap;

    #[test]
    fn test_env_builder_clone() {
        let builder = EnvBuilder::new().configure(|env| env.clone());
        assert_eq!(
            std::env::vars().collect::<HashMap<String, String>>(),
            builder.into()
        );
    }

    #[test]
    fn test_env_builder_add() {
        let mut expected = std::env::vars().collect::<HashMap<String, String>>();
        expected.insert(String::from("MY_TEST_VAR_XYZ"), String::from("MY_VALUE"));
        let builder = EnvBuilder::new().configure(|env| {
            env.clone();
            env.add("MY_TEST_VAR_XYZ", "MY_VALUE");
        });
        assert_eq!(expected, builder.into());
    }

    #[test]
    fn test_env_builder_remove() {
        let mut expected = std::env::vars().collect::<HashMap<String, String>>();
        expected.remove("HOME");
        let builder = EnvBuilder::new().configure(|env| {
            env.clone();
            env.remove("HOME")
        });
        assert_eq!(expected, builder.into());
    }

    #[test]
    fn test_env_builder_clear() {
        let expected: HashMap<String, String> = HashMap::new();
        let builder = EnvBuilder::new().configure(|env| {
            env.clone();
            env.clear();
        });
        assert_eq!(expected, builder.into());
    }
    #[test]
    fn test_env_builder_index_mut() {
        let mut expected: HashMap<String, String> = HashMap::new();
        expected.insert("FOO".into(), "BAR".into());
        expected.insert("BAR".into(), "FOO".into());
        expected.insert("FooBar".into(), "FOO:BAR:".into());

        let builder = EnvBuilder::new().configure(|env| {
            env["FOO"] = "BAR".into();
            env["BAR"] = "FOO".into();
            env["FooBar"] = [&env["BAR"], &env["FOO"], ""].join(":");
        });
        assert_eq!(expected, builder.into());
    }

    #[test]
    fn test_env_builder_configure() {
        let mut expected: HashMap<String, String> = HashMap::new();
        expected.extend(
            vec![
                ("FOO".into(), "BAR".into()),
                ("BAR".into(), "FOO".into()),
                ("MAM".into(), "??".into()),
            ]
            .into_iter(),
        );
        let e = EnvBuilder::new().configure(|env| {
            env.clone();
            env.clear();
            env.add("FOO", "BAR");
            env.add("BAR", "FOO");
            env.add("MAM", "??");
        });
        assert_eq!(expected, e.into());
    }
}
