use std::collections::HashMap;

fn get_input() -> String {
    return "hello world".to_string();
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
let api = "https://v1.jinrishici.com/all";
    let resp = reqwest::blocking::get(api)?
        .json::<HashMap<String, String>>()?;
    println!("{:#?}", resp);
    println!("{}", get_input());
    Ok(())
}