/// Example of cli based provider which serves data from an in memory (Vec) data source
/// on the cli.
///
/// Example usage
/// ```shell
/// user@host ~: cargo run --example cli-provider -- "query { entry(id: 2){weight bodyFat amr bmr } }"
/// ```
use anyhow::Result;
use juniper::{graphql_object, graphql_value, FieldError, FieldResult};
use juniper::{EmptyMutation, EmptySubscription, Variables};
use newton::graphql::{Entry, VecDataProvider};

pub struct Query {}

#[graphql_object(context=VecDataProvider)]
impl Query {
    #[graphql(name = "apiVersion")]
    fn api_version() -> &str {
        "1.0"
    }

    fn entry(context: &VecDataProvider, id: i32) -> FieldResult<Entry> {
        match context.data.iter().skip(id as usize).next().cloned() {
            Some(v) => Ok(v),
            None => Err(FieldError::new("Invalid index", graphql_value!(None))),
        }
    }
}

type Schema<'a> = juniper::RootNode<
    'static,
    Query,
    EmptyMutation<VecDataProvider>,
    EmptySubscription<VecDataProvider>,
>;

fn main() -> Result<()> {
    let args: Vec<String> = std::env::args().collect();

    if args.len() < 2 {
        return Err(anyhow::anyhow!("no query provided"));
    }

    let context = VecDataProvider {
        data: vec![Entry {}, Entry {}, Entry {}, Entry {}],
    };

    let schema = &Schema::new(Query {}, EmptyMutation::new(), EmptySubscription::new());
    let variables = Variables::new();

    // Query Example:
    // "query { entry(id: 2){weight bodyFat amr bmr } }"
    match juniper::execute_sync(&args[1], None, &schema, &variables, &context) {
        Ok((v, errors)) => {
            if !v.is_null() {
                println!("{}", v);
            }
            for e in errors {
                println!("{:?}", e);
            }
        }
        Err(e) => {
            eprintln!("{}", e);
        }
    };
    Ok(())
}
