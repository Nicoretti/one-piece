use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn hello_from_konfy() -> PyResult<String> {
    Ok(String::from("Hello from Konfy"))
}

/// A Python module implemented in Rust.
#[pymodule]
fn konfy(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hello_from_konfy, m)?)?;
    Ok(())
}
