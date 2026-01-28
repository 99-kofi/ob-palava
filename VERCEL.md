# Deploying ObalaPalava to Vercel

The project is now configured for Vercel deployment. Follow these steps to host your app:

## 1. Prepare your Repository
Make sure all your changes (including the new `vercel.json`) are committed to your GitHub repository.

## 2. Import to Vercel
1. Go to [vercel.com](https://vercel.com).
2. Click **Add New** -> **Project**.
3. Import your GitHub repository.

## 3. Configure Environment Variables
Inside the Vercel dashboard, go to **Settings** -> **Environment Variables** and add the following:

| Key | Value |
| :--- | :--- |
| `GEMINI_API_KEY` | Your Google Gemini API Key |
| `YARNGPT_API_KEY` | Your YarnGPT API Key (for Pidgin TTS) |

## 4. Deploy
Click **Deploy**. Vercel will automatically build the Python environment and serve your Flask app.

> [!IMPORTANT]
> **Technical Note on Storage:**
> Since Vercel is a serverless platform, the local SQLite database and generated audio files (TTS) are temporary. They will reset periodically. For a production app with permanent stats, you would eventually need to connect an external database (like Vercel Postgres or MongoDB).
