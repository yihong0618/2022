use anyhow::Result;
use serde::Deserialize;
use clap::{Parser, Args};

static DEFAULT_SENTENCE: &str =
    "赏花归去马如飞\r\n去马如飞酒力微\r\n酒力微醒时已暮\r\n醒时已暮赏花归\r\n";

fn get_input() -> String {
    return "hello world".to_string();
}

#[derive(Debug, Deserialize)]
struct SentenceResponse {
    content: String,
}

async fn get_one_sentence() -> Result<String> {
    let api = "https://v1.jinrishici.com/all";
    let resp = reqwest::get(api).await?.json::<SentenceResponse>().await?;
    Ok(resp.content)
}

#[tokio::main]
async fn main() -> Result<()> {
    let app_opts = AppOpts::parse();
    match app_opts {
        AppOpts::GetUp(get_up_opts) => {
            get_up(get_up_opts).await
        }
    }
    
}

async fn get_up(opts: GetUpOpts) -> Result<()> {
    let sentence = get_one_sentence()
    .await
    .unwrap_or(DEFAULT_SENTENCE.to_string());
    dbg!(sentence);
    Ok(())
}


#[derive(Debug, Parser)]
#[clap(about, version, author)]
enum AppOpts {
    GetUp(GetUpOpts)
}

#[derive(Debug, Args)]
struct GetUpOpts {
    github_token: String,
    repo_name: String,

    /// custom weather message
    wether_message: Option<String>,
    /// telegram bot token
    tele_token: Option<String>,
    /// telegram chat id
    tele_chat_id: Option<String>
}
