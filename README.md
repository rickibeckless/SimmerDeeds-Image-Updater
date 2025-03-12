# **SimmerDeeds Image Updater**

This is a Python-based web scraper that fetches and updates profile images for Simmers (content creators in The Sims community) for my React WebApp **[SimmerDeeds](https://simmerdeeds.netlify.app)** (or *[Repo](https://github.com/rickibeckless/Simmer-Deeds)*). It extracts image URLs from the web page and updates a Supabase database with the latest image links.

## **Features**
- Scrapes images from a given webpage (in this case *[SimmerDeeds](https://simmerdeeds.netlify.app)*).
- Extracts and validates image URLs.
- Updates the Supabase database with new image URLs.
- Handles errors for smooth execution.

## **Requirements**

- Python 3.10+
- `requests`
- `beautifulsoup4`
- `playwright`
- `supabase`
- `python-dotenv`

To install dependencies, run:

```sh
pip install -r requirements.txt
```

## **Environment Variables**

Create a `.env` file in the project root and add the following:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

## **Usage**
1. Ensure the `.env` file is created and the environment variables are set.
2. Install Playwright browsers:

```sh
playwright install
```

3. Run the scraper with:

```sh
python img-desc.py
```

## **Project Structure**

```
simmerdeeds/
│── img-desc.py        # Main script for scraping and updating images
│── .env               # Environment variables
│── requirements.txt   # Dependencies
│── README.md          # Project documentation
```

## **Error Handling**

- If an image is not found, the script skips and logs a message.
- If the Supabase update fails, an error is printed to the console.
