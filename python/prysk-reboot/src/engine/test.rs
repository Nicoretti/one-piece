#[derive(PartialEq, Debug)]
pub struct TestCase {
    name: String,
}

#[derive(Clone)]
pub struct TestCaseBuilder {
    name: String,
}

impl TestCaseBuilder {
    pub fn new(name: &str) -> Self {
        TestCaseBuilder { name: name.into() }
    }

    pub fn name(&mut self, name: &str) -> &Self {
        self.name = String::from(name);
        self
    }
}

impl From<TestCaseBuilder> for TestCase {
    fn from(tc_builder: TestCaseBuilder) -> Self {
        TestCase {
            name: tc_builder.name,
        }
    }
}

impl From<&TestCaseBuilder> for TestCase {
    fn from(tc_builder: &TestCaseBuilder) -> Self {
        TestCase {
            name: tc_builder.name.to_owned(),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn testcase_builder_with_default_settings() {
        let expected = TestCase {
            name: String::from("test"),
        };
        let builder = TestCaseBuilder::new(&String::from("test"));

        assert_eq!(expected, builder.into());
    }
}
