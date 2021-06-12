pub mod graphql {
    use chrono::{DateTime, Utc};
    use juniper::{graphql_object, graphql_value, Context, FieldError, FieldResult};
    use std::iter::Iterator;

    pub trait DataProvider<'a> {
        type IterType: Iterator;
        fn iter(&self) -> Self::IterType;
    }
    impl<'a, I: std::iter::Iterator<Item = &'a Entry>> Context for DataProvider<'a, IterType = I> where
        I: 'a
    {
    }

    pub struct VecDataProvider {
        pub data: Vec<Entry>,
    }

    impl<'a> DataProvider<'a> for VecDataProvider {
        type IterType = std::slice::Iter<'a, Entry>;

        fn iter(&self) -> Self::IterType {
            self.iter()
        }
    }

    #[derive(Copy, Clone)]
    pub struct Entry {}

    #[graphql_object]
    impl Entry {
        pub fn date(&self) -> FieldResult<DateTime<Utc>> {
            Err(FieldError::new("Not Implemented Yet", graphql_value!(None)))
        }

        pub fn weight(&self) -> FieldResult<f64> {
            Ok(0.0)
        }

        pub fn body_fat(&self) -> FieldResult<f64> {
            Ok(0.0)
        }

        pub fn water(&self) -> FieldResult<f64> {
            Ok(0.0)
        }

        pub fn muscles(&self) -> FieldResult<f64> {
            Ok(0.0)
        }

        pub fn bones(&self) -> FieldResult<f64> {
            Ok(0.0)
        }

        pub fn bmr(&self) -> FieldResult<i32> {
            Ok(0i32)
        }

        pub fn amr(&self) -> FieldResult<i32> {
            Ok(0i32)
        }
    }

    #[cfg(test)]
    mod tests {
        #[test]
        fn it_works() {
            assert_eq!(2 + 2, 4);
        }
    }
}
