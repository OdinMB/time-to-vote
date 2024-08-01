## Config

Create a `.env` file based on the `.env.sample` file.

## Development: Install Python Virtual Environment

If you're using a virtual environment (venv) in Python, you'll need to activate it before starting your server. See below for more details.

### Requirements

`pip install` packages as needed in your IDE, then run

    pip freeze > requirements.txt

For easy updates, keep a simple list of packages in `requirements_unfrozen.txt`. To update `requirements.txt`:

    pip uninstall -r requirements.txt -y
    (delete requirements.txt)
    pip install -r requirements_unfrozen.txt
    pip free > requirements.txt

## Deployment

- Build command: `pip install -r requirements.txt`
- Start command: `streamlit run app.py`

Streamlit needs to be deployed in headless mode. Do one of these:

- Set environment variable `STREAMLIT_SERVER_HEADLESS=true`
- Use a parameter in the start command `streamlit run app.py --server.headless true`

## AZURE AUTH

Set the callback URL to `DOMAIN/component/streamlit_oauth.authorize_button/index.html`.

## Appendix

### Development: Install Python Virtual Environment

If you're using a virtual environment (venv) in Python, you'll need to activate it before starting your server. See below for more details.

If you haven't already created a virtual environment, you can do so with:

    python -m venv venv

Activate the virtual environment. The command to do this will depend on your operating system:

On Unix or MacOS, use:

    source venv/bin/activate

On Windows, use:

    .\venv\Scripts\activate

Windows might complain that “running scripts is disabled on this system”. In that case, run the following command:

    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine

Note that this can be a system vulnerability. See https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.4&viewFallbackFrom=powershell-6 for more details.

Once the virtual environment is activated, you'll see (env) before your command prompt. Now you can start your server or install any Python packages and they will be isolated within this environment.
