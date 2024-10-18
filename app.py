
import os
from flask import Flask, render_template, jsonify
import ldclient
from ldclient.config import Config
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)

# Initialize LaunchDarkly client
ld_sdk_key = os.getenv("LAUNCHDARKLY_API_KEY", "YOUR_LAUNCHDARKLY_SDK_KEY")  # Replace with your LaunchDarkly SDK key
ldclient.set_config(Config(ld_sdk_key))

# Feature flag key for the new feature and component
new_feature_flag_key = "new-feature"
component_flag_key = "special-banner-component"

@app.route('/')
def home():
    # User context for LaunchDarkly
    user = {
        "key": "XYZ",  # Replace with actual user key
        "email": "to.charlie.nash@gmail.com"  # Replace with actual user email
    }

    # Check the value of the feature flags
    new_feature_enabled = ldclient.get().variation(new_feature_flag_key, user, False)
    component_enabled = ldclient.get().variation(component_flag_key, user, False)

    # Return both feature flag states to the template
    return render_template("home.html", new_feature=new_feature_enabled, component_enabled=component_enabled)

@app.route('/check-feature-flag')
def check_feature_flag():
    # User context for LaunchDarkly
    user = {
        "key": "XYZ",  # Replace with actual user key
        "email": "to.charlie.nash@gmail.com"  # Replace with actual user email
    }

    # Get the value of the feature flag for instant release/rollback
    new_feature_enabled = ldclient.get().variation(new_feature_flag_key, user, False)

    # Return the feature flag status as JSON
    return jsonify({"new_feature_enabled": new_feature_enabled})

if __name__ == '__main__':
    app.run(debug=True)
