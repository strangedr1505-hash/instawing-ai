# Phone-only setup (Android)

This project is a PWA-style web app. You can deploy it from your phone browser, but it needs a GitHub account and a hosting account. No computer is required.

## A. Upload the project to GitHub using Chrome
1. Extract the ZIP with your Android Files app.
2. Open github.com in Chrome and sign in.
3. Create a new **private** repository named `instawing-ai`.
4. Use **Add file → Upload files**. Upload the project files and folders from the extracted archive. If the mobile page does not support folder upload, use GitHub's browser desktop-site mode or upload files individually.
5. Commit the files to the repository's main branch.

## B. Deploy on Render
1. Open render.com in Chrome and create/sign in to an account.
2. Choose **New → Blueprint** and connect the GitHub repository.
3. Render reads `render.yaml` and creates the web service. Select the free plan if offered.
4. In the service's Environment settings, add `OPENAI_API_KEY` with your own API key. Do not put it in GitHub or share it in chat.
5. Wait for deployment and open the `onrender.com` URL shown by Render.

Free hosting availability, sleep behavior and limits can change. Check the provider's current terms before relying on it.

## C. Install on Android
1. Open the deployed HTTPS URL in Chrome.
2. Open Chrome's three-dot menu.
3. Tap **Add to Home screen** or **Install app**.
4. Launch InstaWing from your home screen.

## D. API key and spending safety
- Create an API key in your OpenAI platform account and add it only as a Render environment variable.
- API usage is billed separately from a ChatGPT subscription.
- Set a low usage budget/alert in your API account if available.
- Never paste your API key into this app's browser fields, GitHub files, or a chat.
- The app sends only the text you type into the AI form to your backend. It does not fetch the Instagram profile link, read DMs, or send messages.
- Local conversation notes stay in this browser's local storage. Clearing browser data removes them.

## E. Important
This is an MVP, not a fully managed hosted service. It does not include user login, server-side conversation storage, Instagram scraping, or automatic messaging. Keep the deployment private while testing and do not enter sensitive personal data.
