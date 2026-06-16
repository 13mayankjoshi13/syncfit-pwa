import json
import os

# Load the generated databases
with open("foods_db.json", "r") as f:
    db_data = json.load(f)

foods_json = json.dumps(db_data["foods"])
exercises_json = json.dumps(db_data["exercises"])

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SyncFit | Health & Fitness Tracker</title>
    
    <!-- PWA Support via inline Base64 manifest -->
    <link rel="manifest" href="data:application/manifest+json;base64,eyJuYW1lIjogIlN5bmNGaXQgSHVhbWFuIFRyYWNrZXIiLCAic2hvcnRfbmFtZSI6ICJTeW5jRml0IiwgImRpc3BsYXkiOiAic3RhbmRhbG9uZSIsICJzdGFydF91cmwiOiAiLiIsICJiYWNrZ3JvdW5kX2NvbG9yIjogIiMwYTBiMGUiLCAidGhlbWVfY29sb3IiOiAiIzBhMGIwZSIsICJpY29ucyI6IFt7InNyYyI6ICJkYXRhOmltYWdlL3N2Zyt4bWw7YmFzZTY0LFBITjJaeUJrWVhSaFBITmhiV1Z6UFNCd2NtOW1hV3hsUFNBOUlqVXdiRDB5TURBZ2IyWm1ZVzEwUFNCeWIyOTBQU0lqTURBOU1UQWdNQ0E1TURBZ2RISmxiV1VpSUhSNWNHVTlSWFpwWlhNZ2RHbHVaM01pSUR4cFkyOXVjeUJ6Y0hKcGMyVnVQR3hsZG1Wc1BHRnlaRzlyWlhKaFkyOTFjbk1pSUR3dmMzWm5QZz09IiwgInNpemVzIjogIjE5MngxOTIiLCAidHlwZSI6ICJpbWFnZS9zdmcreG1sIn1dfQ==">
    <meta name="theme-color" content="#0d0e12">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="description" content="SyncFit: A complete premium Health & Fitness Tracker with LocalStorage. Offline first.">
    
    <style>
        /* CSS RESET & VARS */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }}

        :root {{
            --bg-color: #07080b;
            --bg-radial: radial-gradient(circle at top, #161722 0%, #07080b 100%);
            --card-bg: rgba(18, 20, 29, 0.55);
            --card-bg-hover: rgba(26, 29, 41, 0.75);
            --card-border: rgba(255, 255, 255, 0.06);
            --card-border-focus: rgba(255, 255, 255, 0.15);
            --text-primary: #ffffff;
            --text-secondary: #8e90a6;
            --text-muted: #53556e;
            
            /* Neon gradients */
            --calories-gradient: linear-gradient(135deg, #ff5e62, #ff9966);
            --steps-gradient: linear-gradient(135deg, #10b981, #059669);
            --water-gradient: linear-gradient(135deg, #00f2fe, #4facfe);
            --sleep-gradient: linear-gradient(135deg, #a78bfa, #7c3aed);
            --weight-gradient: linear-gradient(135deg, #f59e0b, #d97706);
            --score-gradient: linear-gradient(135deg, #06b6d4, #0891b2);
            --bg-glow: rgba(255, 255, 255, 0.01);
            
            --accent-primary: #ff5e62;
            --font-stack: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }}

        body {{
            font-family: var(--font-stack);
            background: var(--bg-radial);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
            padding-bottom: 90px; /* Space for bottom nav */
        }}

        /* Typography */
        h1, h2, h3, h4, h5, h6 {{
            font-weight: 600;
            letter-spacing: -0.02em;
        }}

        /* Scrollbar styling */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        ::-webkit-scrollbar-track {{
            background: rgba(255, 255, 255, 0.01);
        }}
        ::-webkit-scrollbar-thumb {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: rgba(255, 255, 255, 0.2);
        }}

        /* Glassmorphism utility */
        .glass-card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 24px;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), background-color 0.3s, border-color 0.3s;
            position: relative;
            overflow: hidden;
        }}
        
        .glass-card::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: radial-gradient(circle at top left, rgba(255, 255, 255, 0.02), transparent);
            pointer-events: none;
            z-index: 0;
        }}

        .glass-card:hover {{
            background: var(--card-bg-hover);
            border-color: var(--card-border-focus);
        }}

        /* Layout Container */
        .container {{
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 24px 16px;
            flex: 1;
        }}

        /* Header Styles */
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            padding: 8px 0;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .brand-logo {{
            width: 36px;
            height: 36px;
            background: var(--calories-gradient);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 12px rgba(255, 94, 98, 0.3);
        }}

        .brand-logo svg {{
            width: 20px;
            height: 20px;
            fill: #fff;
        }}

        .brand-name {{
            font-size: 24px;
            font-weight: 700;
            background: linear-gradient(to right, #fff, var(--text-secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .header-actions {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .date-selector-container {{
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--card-border);
            padding: 8px 12px;
            border-radius: 16px;
        }}

        .date-selector-container input[type="date"] {{
            background: transparent;
            border: none;
            color: #fff;
            font-family: var(--font-stack);
            font-size: 14px;
            font-weight: 600;
            outline: none;
            cursor: pointer;
        }}

        .streak-pill {{
            background: linear-gradient(135deg, rgba(255, 94, 98, 0.1), rgba(255, 153, 102, 0.1));
            border: 1px solid rgba(255, 94, 98, 0.2);
            border-radius: 16px;
            padding: 8px 12px;
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 14px;
            font-weight: 600;
            color: #ff9966;
            cursor: pointer;
        }}

        /* App Sections/Tabs */
        .app-tab {{
            display: none;
            animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .app-tab.active {{
            display: block;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(12px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* DASHBOARD TAB */
        .health-summary-row {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 20px;
            margin-bottom: 24px;
        }}

        @media (min-width: 768px) {{
            .health-summary-row {{
                grid-template-columns: 2fr 3fr;
            }}
        }}

        /* Health Score Card */
        .health-score-card {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 30px;
            text-align: center;
        }}

        .health-score-title {{
            font-size: 18px;
            color: var(--text-secondary);
            margin-bottom: 20px;
        }}

        .score-circle-wrapper {{
            position: relative;
            width: 160px;
            height: 160px;
            margin-bottom: 20px;
        }}

        .score-display {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .score-number {{
            font-size: 42px;
            font-weight: 800;
            line-height: 1;
            background: var(--score-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .score-label {{
            font-size: 12px;
            color: var(--text-muted);
            text-transform: uppercase;
            font-weight: 600;
            margin-top: 4px;
        }}

        /* Grid stats */
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
        }}

        @media (min-width: 480px) {{
            .metrics-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}

        .metric-mini-card {{
            padding: 20px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 150px;
        }}

        .metric-mini-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .metric-icon-circle {{
            width: 36px;
            height: 36px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .metric-mini-title {{
            font-size: 14px;
            color: var(--text-secondary);
            font-weight: 500;
        }}

        .metric-mini-value {{
            font-size: 24px;
            font-weight: 700;
            margin-top: 16px;
        }}

        .metric-mini-progress {{
            width: 100%;
            height: 6px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 3px;
            margin-top: 8px;
            overflow: hidden;
        }}

        .metric-mini-progress-bar {{
            height: 100%;
            border-radius: 3px;
            width: 0%;
            transition: width 0.5s ease-out;
        }}

        .metric-mini-goal {{
            font-size: 11px;
            color: var(--text-muted);
            margin-top: 6px;
            font-weight: 500;
        }}

        /* Macro stats row */
        .macro-row {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-bottom: 24px;
        }}

        .macro-card {{
            padding: 16px;
            text-align: center;
        }}

        .macro-name {{
            font-size: 12px;
            text-transform: uppercase;
            color: var(--text-secondary);
            font-weight: 600;
            margin-bottom: 8px;
        }}

        .macro-value {{
            font-size: 18px;
            font-weight: 700;
        }}

        .macro-progress {{
            height: 4px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 2px;
            margin-top: 10px;
            overflow: hidden;
        }}

        .macro-bar {{
            height: 100%;
            border-radius: 2px;
        }}

        /* Double Column Row */
        .two-col-row {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 20px;
            margin-bottom: 24px;
        }}

        @media (min-width: 768px) {{
            .two-col-row {{
                grid-template-columns: 1fr 1fr;
            }}
        }}

        .coach-card {{
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}

        .coach-header {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .coach-avatar {{
            width: 40px;
            height: 40px;
            border-radius: 14px;
            background: var(--score-gradient);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }}

        .coach-tips-container {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .coach-tip-item {{
            display: flex;
            gap: 10px;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--card-border);
            padding: 12px;
            border-radius: 16px;
            font-size: 13.5px;
            line-height: 1.4;
        }}

        .coach-tip-icon {{
            font-size: 16px;
            flex-shrink: 0;
        }}

        /* Weight Widget */
        .weight-card {{
            padding: 24px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .weight-stats-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin: 16px 0;
        }}

        .weight-stat-box {{
            text-align: center;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--card-border);
            padding: 12px 6px;
            border-radius: 16px;
        }}

        .weight-stat-label {{
            font-size: 11px;
            color: var(--text-secondary);
            margin-bottom: 4px;
        }}

        .weight-stat-value {{
            font-size: 16px;
            font-weight: 700;
        }}

        .bmi-status-badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            margin-top: 10px;
            text-align: center;
            align-self: center;
        }}

        /* DIET & WATER TAB */
        .diet-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 20px;
        }}

        @media (min-width: 900px) {{
            .diet-grid {{
                grid-template-columns: 3fr 2fr;
            }}
        }}

        .meal-log-container {{
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}

        .meal-card {{
            padding: 20px;
        }}

        .meal-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}

        .meal-title-group {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .meal-icon {{
            font-size: 20px;
        }}

        .meal-calories-count {{
            font-size: 14px;
            color: var(--text-secondary);
            font-weight: 500;
        }}

        .meal-items-list {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        .meal-item-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--card-border);
            padding: 10px 14px;
            border-radius: 14px;
        }}

        .meal-item-info {{
            display: flex;
            flex-direction: column;
            gap: 2px;
        }}

        .meal-item-name {{
            font-size: 14px;
            font-weight: 600;
        }}

        .meal-item-sub {{
            font-size: 11px;
            color: var(--text-muted);
        }}

        .meal-item-macros {{
            font-size: 12px;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 16px;
        }}

        .meal-item-delete {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            cursor: pointer;
            padding: 4px;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: color 0.2s, background-color 0.2s;
        }}

        .meal-item-delete:hover {{
            color: #ef4444;
            background: rgba(239, 68, 68, 0.1);
        }}

        .btn-add-food {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px dashed var(--card-border-focus);
            color: var(--text-primary);
            padding: 12px;
            border-radius: 14px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            width: 100%;
            text-align: center;
            transition: background 0.2s;
            margin-top: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }}

        .btn-add-food:hover {{
            background: rgba(255, 255, 255, 0.1);
        }}

        /* Water tracking section */
        .water-track-card {{
            padding: 24px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
        }}

        .water-intake-ring {{
            position: relative;
            width: 140px;
            height: 140px;
        }}

        .water-ring-text {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
        }}

        .water-ring-value {{
            font-size: 24px;
            font-weight: 700;
            color: #4facfe;
        }}

        .water-ring-goal {{
            font-size: 11px;
            color: var(--text-muted);
        }}

        .water-quick-buttons {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            width: 100%;
        }}

        .water-btn {{
            background: rgba(79, 172, 254, 0.1);
            border: 1px solid rgba(79, 172, 254, 0.2);
            color: #4facfe;
            padding: 12px 6px;
            border-radius: 14px;
            font-weight: 700;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s;
            text-align: center;
        }}

        .water-btn:hover {{
            background: #4facfe;
            color: #fff;
            box-shadow: 0 4px 12px rgba(79, 172, 254, 0.3);
        }}

        /* Food Search Drawer / Panel */
        .food-search-card {{
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            height: fit-content;
        }}

        .search-bar-container {{
            position: relative;
        }}

        .search-input {{
            width: 100%;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--card-border);
            border-radius: 14px;
            padding: 12px 16px 12px 40px;
            color: #fff;
            font-family: var(--font-stack);
            font-size: 14px;
            outline: none;
            transition: border-color 0.2s;
        }}

        .search-input:focus {{
            border-color: var(--card-border-focus);
        }}

        .search-icon {{
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-secondary);
            pointer-events: none;
        }}

        .category-filter-pills {{
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding-bottom: 6px;
            mask-image: linear-gradient(to right, black 90%, transparent 100%);
            -webkit-mask-image: linear-gradient(to right, black 90%, transparent 100%);
        }}

        .filter-pill {{
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--card-border);
            color: var(--text-secondary);
            padding: 6px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            white-space: nowrap;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .filter-pill.active {{
            background: var(--calories-gradient);
            border-color: transparent;
            color: #fff;
        }}

        .search-results-list {{
            max-height: 320px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        .search-result-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--card-border);
            padding: 12px;
            border-radius: 16px;
            cursor: pointer;
            transition: background 0.2s;
        }}

        .search-result-item:hover {{
            background: rgba(255, 255, 255, 0.04);
        }}

        .search-result-info {{
            display: flex;
            flex-direction: column;
            gap: 2px;
        }}

        .search-result-name {{
            font-size: 14px;
            font-weight: 600;
        }}

        .search-result-sub {{
            font-size: 11px;
            color: var(--text-muted);
        }}

        .search-result-macros {{
            font-size: 12px;
            font-weight: 700;
            color: var(--text-secondary);
        }}

        /* Log Food Dialog / Modal Overlay */
        .modal-overlay {{
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            z-index: 1000;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 16px;
            animation: fadeIn 0.2s ease-out;
        }}

        .modal-card {{
            width: 100%;
            max-width: 440px;
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            animation: scaleUp 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        }}

        @keyframes scaleUp {{
            from {{ transform: scale(0.9); opacity: 0; }}
            to {{ transform: scale(1); opacity: 1; }}
        }}

        .modal-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .modal-close {{
            background: transparent;
            border: none;
            color: var(--text-secondary);
            font-size: 20px;
            cursor: pointer;
        }}

        .modal-food-name {{
            font-size: 20px;
            font-weight: 700;
        }}

        .modal-food-category {{
            font-size: 12px;
            color: var(--text-muted);
            text-transform: uppercase;
            font-weight: 600;
        }}

        .modal-macros-preview {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--card-border);
            padding: 12px;
            border-radius: 16px;
            text-align: center;
        }}

        .preview-box-label {{
            font-size: 10px;
            color: var(--text-secondary);
            text-transform: uppercase;
            margin-bottom: 4px;
        }}

        .preview-box-val {{
            font-size: 15px;
            font-weight: 700;
        }}

        .serving-selector-row {{
            display: flex;
            gap: 12px;
        }}

        .input-group {{
            display: flex;
            flex-direction: column;
            gap: 6px;
            flex: 1;
        }}

        .input-group label {{
            font-size: 12px;
            color: var(--text-secondary);
            font-weight: 600;
        }}

        .input-group input, .input-group select {{
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 10px;
            color: #fff;
            font-family: var(--font-stack);
            font-size: 14px;
            outline: none;
        }}

        .input-group input:focus, .input-group select:focus {{
            border-color: var(--card-border-focus);
        }}

        .btn-log-action {{
            background: var(--calories-gradient);
            color: #fff;
            border: none;
            padding: 12px;
            border-radius: 14px;
            font-weight: 700;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.2s;
            text-align: center;
        }}

        .btn-log-action:hover {{
            opacity: 0.95;
            box-shadow: 0 4px 12px rgba(255, 94, 98, 0.3);
        }}

        /* WORKOUTS TAB */
        .workout-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 20px;
        }}

        @media (min-width: 900px) {{
            .workout-grid {{
                grid-template-columns: 1fr 1fr;
            }}
        }}

        .log-workout-type-card {{
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            height: fit-content;
        }}

        .workout-nav-pills {{
            display: flex;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 4px;
        }}

        .workout-pill {{
            flex: 1;
            padding: 10px;
            text-align: center;
            border-radius: 12px;
            font-size: 13px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .workout-pill.active {{
            background: rgba(255, 255, 255, 0.08);
            color: #fff;
        }}

        .workout-panel {{
            display: none;
            flex-direction: column;
            gap: 14px;
        }}

        .workout-panel.active {{
            display: flex;
        }}

        .cardio-options-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
        }}

        .cardio-btn {{
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--card-border);
            padding: 12px 6px;
            border-radius: 14px;
            cursor: pointer;
            text-align: center;
            font-size: 12px;
            font-weight: 600;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 6px;
            transition: background 0.2s, border-color 0.2s;
        }}

        .cardio-btn:hover, .cardio-btn.active {{
            background: rgba(255, 94, 98, 0.1);
            border-color: rgba(255, 94, 98, 0.3);
            color: #ff9966;
        }}

        .cardio-icon-large {{
            font-size: 24px;
        }}

        .workout-list-card {{
            padding: 24px;
        }}

        .workout-history-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--card-border);
            padding: 12px 16px;
            border-radius: 16px;
            margin-bottom: 8px;
        }}

        .workout-history-info {{
            display: flex;
            flex-direction: column;
            gap: 2px;
        }}

        .workout-history-name {{
            font-size: 14px;
            font-weight: 600;
        }}

        .workout-history-details {{
            font-size: 11px;
            color: var(--text-secondary);
        }}

        .workout-history-calories {{
            font-size: 13px;
            font-weight: 700;
            color: #ff9966;
        }}

        /* ANALYTICS TAB */
        .analytics-controls {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 12px;
        }}

        .chart-period-selectors, .chart-metric-selectors {{
            display: flex;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 4px;
        }}

        .chart-selector-pill {{
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s;
            color: var(--text-secondary);
        }}

        .chart-selector-pill.active {{
            background: rgba(255, 255, 255, 0.08);
            color: #fff;
        }}

        .chart-canvas-container {{
            width: 100%;
            height: 360px;
            position: relative;
            padding: 10px;
            margin-bottom: 24px;
        }}

        .chart-canvas-container canvas {{
            width: 100%;
            height: 100%;
            display: block;
        }}

        .chart-stats-summary {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
        }}

        .chart-stat-box {{
            text-align: center;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--card-border);
            padding: 16px 8px;
            border-radius: 16px;
        }}

        /* SETTINGS & MORE TAB */
        .settings-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 20px;
        }}

        @media (min-width: 768px) {{
            .settings-grid {{
                grid-template-columns: 1fr 1fr;
            }}
        }}

        .settings-card {{
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 18px;
        }}

        .section-header {{
            font-size: 16px;
            color: var(--text-secondary);
            font-weight: 700;
            border-bottom: 1px solid var(--card-border);
            padding-bottom: 8px;
            margin-bottom: 8px;
        }}

        .backup-buttons {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}

        .btn-profile {{
            background: var(--calories-gradient);
            color: #fff;
            border: none;
            padding: 12px;
            border-radius: 14px;
            font-weight: 700;
            font-size: 14px;
            cursor: pointer;
            width: 100%;
            text-align: center;
        }}

        .btn-secondary {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--card-border);
            color: var(--text-primary);
            padding: 12px;
            border-radius: 14px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            width: 100%;
            text-align: center;
            transition: all 0.2s;
        }}

        .btn-secondary:hover {{
            background: rgba(255, 255, 255, 0.1);
        }}

        .btn-danger {{
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid rgba(239, 68, 68, 0.3);
            color: #ef4444;
            padding: 12px;
            border-radius: 14px;
            font-weight: 700;
            font-size: 14px;
            cursor: pointer;
            width: 100%;
            text-align: center;
            transition: all 0.2s;
        }}

        .btn-danger:hover {{
            background: #ef4444;
            color: #fff;
        }}

        /* Daily Notes widget */
        .notes-textarea {{
            width: 100%;
            height: 100px;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 12px;
            color: #fff;
            font-family: var(--font-stack);
            font-size: 13.5px;
            outline: none;
            resize: none;
            transition: border-color 0.2s;
        }}

        .notes-textarea:focus {{
            border-color: var(--card-border-focus);
        }}

        /* Achievements Gallery in settings */
        .achievements-gallery {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            margin-top: 10px;
        }}

        @media (max-width: 480px) {{
            .achievements-gallery {{
                grid-template-columns: repeat(3, 1fr);
            }}
        }}

        .achievement-badge {{
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            cursor: pointer;
            opacity: 0.35;
            transition: opacity 0.3s, transform 0.3s;
        }}

        .achievement-badge.unlocked {{
            opacity: 1;
            transform: scale(1);
        }}

        .achievement-badge.unlocked:hover {{
            transform: scale(1.08);
        }}

        .badge-icon-holder {{
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.03);
            border: 2px solid var(--card-border);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            margin-bottom: 6px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            transition: all 0.3s;
        }}

        .achievement-badge.unlocked .badge-icon-holder {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.01));
            border-color: #f59e0b;
            box-shadow: 0 0 15px rgba(245, 158, 11, 0.3);
        }}

        .badge-label {{
            font-size: 10px;
            font-weight: 700;
            color: var(--text-secondary);
            max-width: 70px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}

        /* Achievement Unlock Modal */
        .achievement-popup {{
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0, 0, 0, 0.85);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            z-index: 2000;
            display: none;
            align-items: center;
            justify-content: center;
            animation: fadeIn 0.3s ease-out;
        }}

        .achievement-popup-card {{
            width: 100%;
            max-width: 380px;
            padding: 40px 24px;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
            animation: bounceIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}

        @keyframes bounceIn {{
            0% {{ transform: scale(0.3); opacity: 0; }}
            50% {{ transform: scale(1.05); opacity: 0.8; }}
            70% {{ transform: scale(0.9); opacity: 0.9; }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}

        .popup-badge-icon {{
            width: 100px;
            height: 100px;
            border-radius: 50%;
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(245, 158, 11, 0.05));
            border: 3px solid #f59e0b;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 50px;
            box-shadow: 0 0 30px rgba(245, 158, 11, 0.5);
            margin-bottom: 10px;
            animation: spinGlow 4s infinite linear;
        }}

        @keyframes spinGlow {{
            0% {{ transform: rotate(0deg); box-shadow: 0 0 30px rgba(245, 158, 11, 0.4); }}
            50% {{ box-shadow: 0 0 45px rgba(245, 158, 11, 0.7); }}
            100% {{ transform: rotate(360deg); box-shadow: 0 0 30px rgba(245, 158, 11, 0.4); }}
        }}

        .popup-title {{
            font-size: 24px;
            font-weight: 800;
            background: linear-gradient(to right, #fff, #f59e0b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .popup-desc {{
            font-size: 14px;
            color: var(--text-secondary);
            line-height: 1.5;
        }}

        /* Floating Bottom Navigation */
        .bottom-nav-container {{
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            width: 90%;
            max-width: 440px;
            z-index: 900;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }}

        .bottom-nav {{
            display: flex;
            justify-content: space-around;
            align-items: center;
            padding: 10px 14px;
            border-radius: 20px;
        }}

        .nav-item {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            color: var(--text-secondary);
            text-decoration: none;
            cursor: pointer;
            transition: all 0.2s;
            flex: 1;
        }}

        .nav-item svg {{
            width: 20px;
            height: 20px;
            stroke: currentColor;
            stroke-width: 2.2;
            fill: none;
            transition: transform 0.2s;
        }}

        .nav-item.active {{
            color: var(--accent-primary);
        }}

        .nav-item.active svg {{
            transform: translateY(-2px);
        }}

        .nav-label {{
            font-size: 10px;
            font-weight: 700;
        }}

        /* Utility classes */
        .d-flex {{ display: flex; }}
        .flex-col {{ flex-direction: column; }}
        .align-center {{ align-items: center; }}
        .justify-between {{ justify-content: space-between; }}
        .w-100 {{ width: 100%; }}
        .gap-12 {{ gap: 12px; }}
        
        /* Interactive counters styling */
        .counter-animate {{
            transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
        }}
    </style>
</head>
<body>

    <div class="container">
        <!-- HEADER -->
        <header>
            <div class="brand">
                <div class="brand-logo">
                    <svg viewBox="0 0 24 24">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15.5h-2v-2h2v2zm0-4h-2v-6h2v6z"/>
                    </svg>
                </div>
                <div class="brand-name">SyncFit</div>
            </div>
            
            <div class="header-actions">
                <div class="streak-pill" id="header-streak" onclick="switchTab('settings')">
                    ⚡ <span id="streak-count-val">0</span>d
                </div>
                <div class="date-selector-container">
                    <input type="date" id="active-date-picker">
                </div>
            </div>
        </header>

        <!-- DASHBOARD TAB -->
        <div id="tab-dashboard" class="app-tab active">
            <div class="health-summary-row">
                <!-- Health Score ring card -->
                <div class="glass-card health-score-card">
                    <div class="health-score-title">Daily Health Score</div>
                    <div class="score-circle-wrapper">
                        <svg class="progress-ring" width="160" height="160">
                            <defs>
                                <linearGradient id="grad-score" x1="0%" y1="0%" x2="100%" y2="100%">
                                    <stop offset="0%" stop-color="#06b6d4" />
                                    <stop offset="100%" stop-color="#0891b2" />
                                </linearGradient>
                            </defs>
                            <circle stroke="rgba(255,255,255,0.03)" stroke-width="12" fill="transparent" r="70" cx="80" cy="80"/>
                            <circle id="score-ring-circle" stroke="url(#grad-score)" stroke-width="12" fill="transparent" r="70" cx="80" cy="80" stroke-linecap="round" stroke-dasharray="439.8" stroke-dashoffset="439.8"/>
                        </svg>
                        <div class="score-display">
                            <span class="score-number counter-animate" id="health-score-val">0</span>
                            <span class="score-label">Points</span>
                        </div>
                    </div>
                    <p style="font-size: 13px; color: var(--text-secondary); line-height: 1.4;">Based on Calories, Steps, Water, Sleep, and Activity targets.</p>
                </div>

                <!-- Metrics Grid -->
                <div class="metrics-grid">
                    <!-- Calories Card -->
                    <div class="glass-card metric-mini-card" onclick="switchTab('diet')">
                        <div class="metric-mini-header">
                            <span class="metric-mini-title">Net Calories</span>
                            <div class="metric-icon-circle" style="background: rgba(255, 94, 98, 0.1);">
                                🍎
                            </div>
                        </div>
                        <div>
                            <div class="metric-mini-value" id="net-calories-val">0 kcal</div>
                            <div class="metric-mini-progress">
                                <div class="metric-mini-progress-bar" id="calories-progress-bar" style="background: var(--calories-gradient);"></div>
                            </div>
                            <div class="metric-mini-goal" id="calories-goal-text">Goal: 2200 kcal</div>
                        </div>
                    </div>

                    <!-- Steps Card -->
                    <div class="glass-card metric-mini-card" onclick="openStepsLogger()">
                        <div class="metric-mini-header">
                            <span class="metric-mini-title">Steps Walked</span>
                            <div class="metric-icon-circle" style="background: rgba(16, 185, 129, 0.1);">
                                👟
                            </div>
                        </div>
                        <div>
                            <div class="metric-mini-value" id="steps-val">0</div>
                            <div class="metric-mini-progress">
                                <div class="metric-mini-progress-bar" id="steps-progress-bar" style="background: var(--steps-gradient);"></div>
                            </div>
                            <div class="metric-mini-goal" id="steps-goal-text">Goal: 10,000</div>
                        </div>
                    </div>

                    <!-- Water Card -->
                    <div class="glass-card metric-mini-card" onclick="switchTab('diet')">
                        <div class="metric-mini-header">
                            <span class="metric-mini-title">Water Logged</span>
                            <div class="metric-icon-circle" style="background: rgba(0, 242, 254, 0.1);">
                                💧
                            </div>
                        </div>
                        <div>
                            <div class="metric-mini-value" id="water-val">0 ml</div>
                            <div class="metric-mini-progress">
                                <div class="metric-mini-progress-bar" id="water-progress-bar" style="background: var(--water-gradient);"></div>
                            </div>
                            <div class="metric-mini-goal" id="water-goal-text">Goal: 3,000 ml</div>
                        </div>
                    </div>

                    <!-- Sleep Card -->
                    <div class="glass-card metric-mini-card" onclick="openSleepLogger()">
                        <div class="metric-mini-header">
                            <span class="metric-mini-title">Sleep Duration</span>
                            <div class="metric-icon-circle" style="background: rgba(167, 139, 250, 0.1);">
                                😴
                            </div>
                        </div>
                        <div>
                            <div class="metric-mini-value" id="sleep-val">0h</div>
                            <div class="metric-mini-progress">
                                <div class="metric-mini-progress-bar" id="sleep-progress-bar" style="background: var(--sleep-gradient);"></div>
                            </div>
                            <div class="metric-mini-goal" id="sleep-goal-text">Goal: 8.0h</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Macros Bar Widget -->
            <div class="glass-card macro-row">
                <div class="macro-card">
                    <div class="macro-name" style="color: #ff5e62;">Protein</div>
                    <div class="macro-value" id="macro-protein-val">0g</div>
                    <div class="macro-progress">
                        <div class="macro-bar" id="protein-bar" style="background: #ff5e62; width: 0%;"></div>
                    </div>
                </div>
                <div class="macro-card">
                    <div class="macro-name" style="color: #06b6d4;">Carbs</div>
                    <div class="macro-value" id="macro-carbs-val">0g</div>
                    <div class="macro-progress">
                        <div class="macro-bar" id="carbs-bar" style="background: #06b6d4; width: 0%;"></div>
                    </div>
                </div>
                <div class="macro-card">
                    <div class="macro-name" style="color: #f59e0b;">Fat</div>
                    <div class="macro-value" id="macro-fat-val">0g</div>
                    <div class="macro-progress">
                        <div class="macro-bar" id="fat-bar" style="background: #f59e0b; width: 0%;"></div>
                    </div>
                </div>
            </div>

            <!-- AI Coach & Weight row -->
            <div class="two-col-row">
                <!-- AI Coach card -->
                <div class="glass-card coach-card">
                    <div class="coach-header">
                        <div class="coach-avatar">🤖</div>
                        <div>
                            <h4 style="font-size: 15px; font-weight:700;">AI Coaching Feed</h4>
                            <span style="font-size: 11px; color: var(--text-muted);">Real-time fitness guidance</span>
                        </div>
                    </div>
                    <div class="coach-tips-container" id="coach-tips-feed">
                        <!-- Tips are generated dynamically in JS -->
                    </div>
                </div>

                <!-- Weight and BMI Card -->
                <div class="glass-card weight-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="font-size: 16px; font-weight:700;">Weight & BMI Tracker</h4>
                        <button class="btn-secondary" style="width: auto; padding: 6px 12px; font-size: 11px; border-radius: 10px;" onclick="openWeightLogger()">Update</button>
                    </div>
                    
                    <div class="weight-stats-grid">
                        <div class="weight-stat-box">
                            <div class="weight-stat-label">Current</div>
                            <div class="weight-stat-value" id="weight-current-val">-- kg</div>
                        </div>
                        <div class="weight-stat-box">
                            <div class="weight-stat-label">Goal</div>
                            <div class="weight-stat-value" id="weight-goal-val">-- kg</div>
                        </div>
                        <div class="weight-stat-box">
                            <div class="weight-stat-label">BMI</div>
                            <div class="weight-stat-value" id="bmi-val">--</div>
                        </div>
                    </div>

                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 12px; color: var(--text-secondary);" id="weight-diff-text">Weight change: --</span>
                        <div class="bmi-status-badge" id="bmi-badge">--</div>
                    </div>
                </div>
            </div>

            <!-- Notes Section -->
            <div class="glass-card" style="padding: 20px; margin-bottom: 20px;">
                <h4 style="font-size: 15px; font-weight:700; margin-bottom: 10px;">Daily Fitness Notes</h4>
                <textarea id="daily-notes-input" class="notes-textarea" placeholder="How did you feel today? Log training remarks, energy levels, or hydration feel..."></textarea>
            </div>
        </div>

        <!-- DIET & WATER TAB -->
        <div id="tab-diet" class="app-tab">
            <div class="diet-grid">
                <!-- Log List Container -->
                <div class="meal-log-container">
                    <!-- Breakfast Card -->
                    <div class="glass-card meal-card">
                        <div class="meal-card-header">
                            <div class="meal-title-group">
                                <span class="meal-icon">🥞</span>
                                <h3 style="font-size: 16px; font-weight: 700;">Breakfast</h3>
                            </div>
                            <span class="meal-calories-count" id="breakfast-cal-total">0 kcal</span>
                        </div>
                        <div class="meal-items-list" id="breakfast-items-list">
                            <!-- Items added dynamically -->
                        </div>
                        <button class="btn-add-food" onclick="openFoodSearch('Breakfast')">➕ Add breakfast food</button>
                    </div>

                    <!-- Lunch Card -->
                    <div class="glass-card meal-card">
                        <div class="meal-card-header">
                            <div class="meal-title-group">
                                <span class="meal-icon">🍱</span>
                                <h3 style="font-size: 16px; font-weight: 700;">Lunch</h3>
                            </div>
                            <span class="meal-calories-count" id="lunch-cal-total">0 kcal</span>
                        </div>
                        <div class="meal-items-list" id="lunch-items-list">
                            <!-- Items added dynamically -->
                        </div>
                        <button class="btn-add-food" onclick="openFoodSearch('Lunch')">➕ Add lunch food</button>
                    </div>

                    <!-- Dinner Card -->
                    <div class="glass-card meal-card">
                        <div class="meal-card-header">
                            <div class="meal-title-group">
                                <span class="meal-icon">🥘</span>
                                <h3 style="font-size: 16px; font-weight: 700;">Dinner</h3>
                            </div>
                            <span class="meal-calories-count" id="dinner-cal-total">0 kcal</span>
                        </div>
                        <div class="meal-items-list" id="dinner-items-list">
                            <!-- Items added dynamically -->
                        </div>
                        <button class="btn-add-food" onclick="openFoodSearch('Dinner')">➕ Add dinner food</button>
                    </div>

                    <!-- Snacks Card -->
                    <div class="glass-card meal-card">
                        <div class="meal-card-header">
                            <div class="meal-title-group">
                                <span class="meal-icon">🍎</span>
                                <h3 style="font-size: 16px; font-weight: 700;">Snacks</h3>
                            </div>
                            <span class="meal-calories-count" id="snacks-cal-total">0 kcal</span>
                        </div>
                        <div class="meal-items-list" id="snacks-items-list">
                            <!-- Items added dynamically -->
                        </div>
                        <button class="btn-add-food" onclick="openFoodSearch('Snacks')">➕ Add snacks food</button>
                    </div>
                </div>

                <!-- Right Side: Food Search panel and Water Card -->
                <div class="flex-col gap-12" style="display: flex;">
                    <!-- Water Track Widget -->
                    <div class="glass-card water-track-card">
                        <h3 style="font-size: 16px; font-weight: 700; width: 100%;">Water Hydration</h3>
                        <div class="water-intake-ring">
                            <svg class="progress-ring" width="140" height="140">
                                <defs>
                                    <linearGradient id="grad-water" x1="0%" y1="0%" x2="100%" y2="100%">
                                        <stop offset="0%" stop-color="#00f2fe" />
                                        <stop offset="100%" stop-color="#4facfe" />
                                    </linearGradient>
                                </defs>
                                <circle stroke="rgba(255,255,255,0.03)" stroke-width="10" fill="transparent" r="60" cx="70" cy="70"/>
                                <circle id="water-ring-circle" stroke="url(#grad-water)" stroke-width="10" fill="transparent" r="60" cx="70" cy="70" stroke-linecap="round" stroke-dasharray="377" stroke-dashoffset="377"/>
                            </svg>
                            <div class="water-ring-text">
                                <div class="water-ring-value" id="water-tab-val">0</div>
                                <div class="water-ring-goal" id="water-tab-goal-text">of 3.0L</div>
                            </div>
                        </div>
                        <div class="water-quick-buttons">
                            <button class="water-btn" onclick="addWater(250)">+250ml</button>
                            <button class="water-btn" onclick="addWater(500)">+500ml</button>
                            <button class="water-btn" onclick="addWater(1000)">+1.0 L</button>
                        </div>
                    </div>

                    <!-- Food Search / Built-in Database -->
                    <div class="glass-card food-search-card" id="food-search-panel">
                        <h3 style="font-size: 16px; font-weight: 700;">Food Database</h3>
                        <div class="search-bar-container">
                            <input type="text" id="food-search-input" class="search-input" placeholder="Search 500+ foods...">
                            <span class="search-icon">🔍</span>
                        </div>
                        <div class="category-filter-pills" id="food-category-filters">
                            <!-- Category Pills generated in JS -->
                        </div>
                        <div class="search-results-list" id="food-search-results">
                            <!-- Search results generated dynamically -->
                        </div>
                        <button class="btn-secondary" onclick="openCustomFoodModal()" style="margin-top: 10px; font-size: 13px; font-weight: 700;">➕ Log Custom Food Item</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- WORKOUTS TAB -->
        <div id="tab-workouts" class="app-tab">
            <div class="workout-grid">
                <!-- Log workout widget -->
                <div class="glass-card log-workout-type-card">
                    <h3 style="font-size: 16px; font-weight: 700; margin-bottom: 8px;">Log Physical Activity</h3>
                    
                    <div class="workout-nav-pills">
                        <div class="workout-pill active" id="pill-cardio" onclick="toggleWorkoutType('cardio')">Cardio Training</div>
                        <div class="workout-pill" id="pill-gym" onclick="toggleWorkoutType('gym')">Resistance / Gym</div>
                    </div>

                    <!-- Cardio workout logger -->
                    <div class="workout-panel active" id="panel-cardio">
                        <div class="cardio-options-grid">
                            <button class="cardio-btn active" onclick="selectCardio('Walking', '👟')">
                                <span class="cardio-icon-large">👟</span>
                                <span>Walking</span>
                            </button>
                            <button class="cardio-btn" onclick="selectCardio('Running', '🏃')">
                                <span class="cardio-icon-large">🏃</span>
                                <span>Running</span>
                            </button>
                            <button class="cardio-btn" onclick="selectCardio('Cycling', '🚴')">
                                <span class="cardio-icon-large">🚴</span>
                                <span>Cycling</span>
                            </button>
                            <button class="cardio-btn" onclick="selectCardio('Swimming', '🏊')">
                                <span class="cardio-icon-large">🏊</span>
                                <span>Swimming</span>
                            </button>
                            <button class="cardio-btn" onclick="selectCardio('Yoga', '🧘')">
                                <span class="cardio-icon-large">🧘</span>
                                <span>Yoga</span>
                            </button>
                            <button class="cardio-btn" onclick="selectCardio('Sports', '⚽')">
                                <span class="cardio-icon-large">⚽</span>
                                <span>Sports</span>
                            </button>
                        </div>

                        <!-- Dynamic Cardio Fields -->
                        <div id="cardio-fields-container" class="flex-col gap-12" style="display: flex;">
                            <!-- Handled in JS based on selection -->
                        </div>

                        <button class="btn-log-action" style="margin-top: 10px;" onclick="logCardioSession()">Log Cardio Activity</button>
                    </div>

                    <!-- Gym workout logger -->
                    <div class="workout-panel" id="panel-gym">
                        <div class="input-group">
                            <label for="gym-muscle-select">Select Muscle Group</label>
                            <select id="gym-muscle-select" onchange="filterGymExercises()">
                                <option value="Chest">Chest</option>
                                <option value="Back">Back</option>
                                <option value="Shoulders">Shoulders</option>
                                <option value="Biceps">Biceps</option>
                                <option value="Triceps">Triceps</option>
                                <option value="Legs">Legs</option>
                                <option value="Core">Core</option>
                            </select>
                        </div>
                        <div class="input-group">
                            <label for="gym-exercise-select">Select Exercise</label>
                            <select id="gym-exercise-select">
                                <!-- Loaded in JS -->
                            </select>
                        </div>
                        
                        <div class="serving-selector-row">
                            <div class="input-group">
                                <label for="gym-sets">Sets</label>
                                <input type="number" id="gym-sets" value="4" min="1" max="20">
                            </div>
                            <div class="input-group">
                                <label for="gym-reps">Reps</label>
                                <input type="number" id="gym-reps" value="10" min="1" max="100">
                            </div>
                            <div class="input-group">
                                <label for="gym-weight">Weight (kg)</label>
                                <input type="number" id="gym-weight" value="40" min="0" max="500">
                            </div>
                        </div>

                        <div class="input-group">
                            <label for="gym-duration">Duration (minutes)</label>
                            <input type="number" id="gym-duration" value="30" min="1" max="300">
                        </div>

                        <button class="btn-log-action" style="margin-top: 10px;" onclick="logGymWorkout()">Log Sets & Reps</button>
                    </div>
                </div>

                <!-- Today's logged activities -->
                <div class="glass-card workout-list-card">
                    <div class="meal-card-header">
                        <h3 style="font-size: 16px; font-weight: 700;">Workout Sessions</h3>
                        <span class="meal-calories-count" id="workouts-burned-total">0 kcal burned</span>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 12px;" id="logged-workouts-list">
                        <!-- Loaded dynamically -->
                    </div>
                </div>
            </div>
        </div>

        <!-- ANALYTICS TAB -->
        <div id="tab-analytics" class="app-tab">
            <div class="glass-card" style="padding: 20px; margin-bottom: 20px;">
                <div class="analytics-controls">
                    <h3 style="font-size: 16px; font-weight: 700;">Visual Health Trends</h3>
                    
                    <!-- Metrics selectors -->
                    <div class="chart-metric-selectors">
                        <select id="chart-metric-dropdown" style="background: transparent; border: none; color: #fff; font-weight: 700; outline: none; font-size: 12px; font-family: var(--font-stack);" onchange="drawAnalyticsChart()">
                            <option value="Weight">Weight Trend</option>
                            <option value="Calories">Calorie Balance</option>
                            <option value="Burned">Calories Burned</option>
                            <option value="Protein">Protein Intake</option>
                            <option value="Water">Water Hydration</option>
                            <option value="Steps">Steps Progress</option>
                            <option value="Sleep">Sleep Trend</option>
                        </select>
                    </div>

                    <!-- Period selector -->
                    <div class="chart-period-selectors" id="chart-period-container">
                        <div class="chart-selector-pill active" onclick="setChartPeriod(7)">7d</div>
                        <div class="chart-selector-pill" onclick="setChartPeriod(30)">30d</div>
                        <div class="chart-selector-pill" onclick="setChartPeriod(90)">90d</div>
                    </div>
                </div>

                <!-- Pure HTML Canvas Chart Wrapper -->
                <div class="chart-canvas-container">
                    <canvas id="analytics-canvas"></canvas>
                </div>

                <!-- Stats summary below chart -->
                <div class="chart-stats-summary" id="chart-stats-summary-grid">
                    <div class="chart-stat-box">
                        <div class="weight-stat-label">Average</div>
                        <div class="weight-stat-value" id="chart-avg-val">--</div>
                    </div>
                    <div class="chart-stat-box">
                        <div class="weight-stat-label">Minimum</div>
                        <div class="weight-stat-value" id="chart-min-val">--</div>
                    </div>
                    <div class="chart-stat-box">
                        <div class="weight-stat-label">Maximum</div>
                        <div class="weight-stat-value" id="chart-max-val">--</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- SETTINGS & MORE TAB -->
        <div id="tab-settings" class="app-tab">
            <div class="settings-grid">
                <!-- Target Profiles config -->
                <div class="glass-card settings-card">
                    <div class="section-header">Target Configuration</div>
                    
                    <div class="serving-selector-row">
                        <div class="input-group">
                            <label for="profile-height">Height (cm)</label>
                            <input type="number" id="profile-height" value="175" min="100" max="250" onchange="saveProfileSettings()">
                        </div>
                        <div class="input-group">
                            <label for="profile-weight">Weight (kg)</label>
                            <input type="number" id="profile-weight" value="70" min="20" max="300" onchange="saveProfileSettings()">
                        </div>
                        <div class="input-group">
                            <label for="profile-goal-weight">Goal Weight (kg)</label>
                            <input type="number" id="profile-goal-weight" value="65" min="20" max="300" onchange="saveProfileSettings()">
                        </div>
                    </div>

                    <div class="serving-selector-row">
                        <div class="input-group">
                            <label for="profile-calories">Calorie Goal (kcal)</label>
                            <input type="number" id="profile-calories" value="2200" min="500" max="10000" onchange="saveProfileSettings()">
                        </div>
                        <div class="input-group">
                            <label for="profile-water">Water Goal (ml)</label>
                            <input type="number" id="profile-water" value="3000" min="500" max="10000" onchange="saveProfileSettings()">
                        </div>
                    </div>

                    <div class="serving-selector-row">
                        <div class="input-group">
                            <label for="profile-steps">Steps Goal</label>
                            <input type="number" id="profile-steps" value="10000" min="1000" max="100000" onchange="saveProfileSettings()">
                        </div>
                        <div class="input-group">
                            <label for="profile-sleep">Sleep Goal (hours)</label>
                            <input type="number" id="profile-sleep" value="8" min="3" max="24" step="0.5" onchange="saveProfileSettings()">
                        </div>
                    </div>
                </div>

                <!-- Backup and Achievements -->
                <div class="flex-col gap-12" style="display: flex;">
                    <!-- Achievements Panel -->
                    <div class="glass-card settings-card">
                        <div class="section-header" style="display:flex; justify-content:space-between; align-items:center;">
                            <span>Milestone Achievements</span>
                            <span style="font-size: 11px; font-weight:700; color:#f59e0b;" id="unlocked-badge-count">0/11 Unlocked</span>
                        </div>
                        <div class="achievements-gallery" id="achievements-gallery-grid">
                            <!-- Badges loaded dynamically in JS -->
                        </div>
                    </div>

                    <!-- Backup tools -->
                    <div class="glass-card settings-card">
                        <div class="section-header">Database Management</div>
                        <div class="backup-buttons">
                            <button class="btn-secondary" onclick="exportBackupData()">💾 Export Backup (JSON)</button>
                            <button class="btn-secondary" onclick="document.getElementById('import-file-input').click()">📂 Import Backup (JSON)</button>
                            <input type="file" id="import-file-input" style="display: none;" accept=".json" onchange="importBackupData(event)">
                            <button class="btn-danger" onclick="resetAllTrackerData()">⚠️ Reset All Tracker Data</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- FLOATING BOTTOM NAVIGATION -->
    <div class="bottom-nav-container">
        <div class="glass-card bottom-nav">
            <div class="nav-item active" id="nav-dashboard" onclick="switchTab('dashboard')">
                <svg viewBox="0 0 24 24">
                    <rect x="3" y="3" width="7" height="7" rx="1.5" />
                    <rect x="14" y="3" width="7" height="7" rx="1.5" />
                    <rect x="14" y="14" width="7" height="7" rx="1.5" />
                    <rect x="3" y="14" width="7" height="7" rx="1.5" />
                </svg>
                <span class="nav-label">Dashboard</span>
            </div>
            <div class="nav-item" id="nav-diet" onclick="switchTab('diet')">
                <svg viewBox="0 0 24 24">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17h-2v-2h2v2zm0-4h-2v-4h2v4zm0-6h-2V7h2v2z"/>
                </svg>
                <span class="nav-label">Diet & Log</span>
            </div>
            <div class="nav-item" id="nav-workouts" onclick="switchTab('workouts')">
                <svg viewBox="0 0 24 24">
                    <path d="M6.5 12a5.5 5.5 0 1 1 11 0 5.5 5.5 0 0 1-11 0zm5.5-3.5a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm0 9a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm4.5-4.5a1 1 0 1 0-2 0 1 1 0 0 0 2 0zm-9 0a1 1 0 1 0-2 0 1 1 0 0 0 2 0z"/>
                </svg>
                <span class="nav-label">Workouts</span>
            </div>
            <div class="nav-item" id="nav-analytics" onclick="switchTab('analytics')">
                <svg viewBox="0 0 24 24">
                    <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>
                </svg>
                <span class="nav-label">Analytics</span>
            </div>
            <div class="nav-item" id="nav-settings" onclick="switchTab('settings')">
                <svg viewBox="0 0 24 24">
                    <circle cx="12" cy="12" r="3"/>
                    <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
                </svg>
                <span class="nav-label">Settings</span>
            </div>
        </div>
    </div>

    <!-- LOG FOOD MODAL -->
    <div class="modal-overlay" id="log-food-modal">
        <div class="glass-card modal-card">
            <div class="modal-header">
                <div>
                    <div class="modal-food-category" id="modal-item-category">Category</div>
                    <div class="modal-food-name" id="modal-item-name">Food Item Name</div>
                </div>
                <button class="modal-close" onclick="closeFoodModal()">✕</button>
            </div>
            
            <div class="modal-macros-preview">
                <div>
                    <div class="preview-box-label">Calories</div>
                    <div class="preview-box-val" id="modal-preview-cal" style="color: #ff5e62;">0</div>
                </div>
                <div>
                    <div class="preview-box-label">Protein</div>
                    <div class="preview-box-val" id="modal-preview-prot" style="color: #ff5e62;">0g</div>
                </div>
                <div>
                    <div class="preview-box-label">Carbs</div>
                    <div class="preview-box-val" id="modal-preview-carb" style="color: #06b6d4;">0g</div>
                </div>
                <div>
                    <div class="preview-box-label">Fat</div>
                    <div class="preview-box-val" id="modal-preview-fat" style="color: #f59e0b;">0g</div>
                </div>
            </div>

            <div class="serving-selector-row">
                <div class="input-group">
                    <label for="modal-quantity">Quantity</label>
                    <input type="number" id="modal-quantity" value="1" min="0.1" max="100" step="0.1" oninput="calculateModalMacros()">
                </div>
                <div class="input-group">
                    <label for="modal-serving-size">Serving Unit</label>
                    <select id="modal-serving-size" onchange="calculateModalMacros()">
                        <!-- Loaded dynamically -->
                    </select>
                </div>
            </div>

            <div class="input-group">
                <label for="modal-meal-type">Logged Meal</label>
                <select id="modal-meal-type">
                    <option value="Breakfast">Breakfast</option>
                    <option value="Lunch">Lunch</option>
                    <option value="Dinner">Dinner</option>
                    <option value="Snacks">Snacks</option>
                </select>
            </div>

            <button class="btn-log-action" onclick="addFoodToLog()">Log Food Item</button>
        </div>
    </div>

    <!-- LOG STEPS MODAL -->
    <div class="modal-overlay" id="log-steps-modal">
        <div class="glass-card modal-card">
            <div class="modal-header">
                <div>
                    <div class="modal-food-category">Manual Tracking</div>
                    <div class="modal-food-name">Log Daily Steps</div>
                </div>
                <button class="modal-close" onclick="closeStepsLogger()">✕</button>
            </div>
            
            <div class="input-group">
                <label for="manual-steps-input">Steps Counted</label>
                <input type="number" id="manual-steps-input" value="6000" min="0" max="100000" step="100">
            </div>

            <button class="btn-log-action" onclick="saveManualSteps()">Save Steps</button>
        </div>
    </div>

    <!-- LOG SLEEP MODAL -->
    <div class="modal-overlay" id="log-sleep-modal">
        <div class="glass-card modal-card">
            <div class="modal-header">
                <div>
                    <div class="modal-food-category">Manual Tracking</div>
                    <div class="modal-food-name">Log Night Sleep</div>
                </div>
                <button class="modal-close" onclick="closeSleepLogger()">✕</button>
            </div>
            
            <div class="serving-selector-row">
                <div class="input-group">
                    <label for="manual-sleep-hours">Hours Slept</label>
                    <input type="number" id="manual-sleep-hours" value="8" min="0.5" max="24" step="0.5">
                </div>
                <div class="input-group">
                    <label for="manual-sleep-quality">Sleep Quality</label>
                    <select id="manual-sleep-quality">
                        <option value="Excellent">Excellent</option>
                        <option value="Good" selected>Good</option>
                        <option value="Poor">Poor</option>
                    </select>
                </div>
            </div>

            <button class="btn-log-action" onclick="saveManualSleep()">Save Sleep Log</button>
        </div>
    </div>

    <!-- UPDATE WEIGHT MODAL -->
    <div class="modal-overlay" id="log-weight-modal">
        <div class="glass-card modal-card">
            <div class="modal-header">
                <div>
                    <div class="modal-food-category">Body Measurements</div>
                    <div class="modal-food-name">Update Today's Weight</div>
                </div>
                <button class="modal-close" onclick="closeWeightLogger()">✕</button>
            </div>
            
            <div class="input-group">
                <label for="manual-weight-input">Weight (kg)</label>
                <input type="number" id="manual-weight-input" value="70" min="20" max="300" step="0.1">
            </div>

            <button class="btn-log-action" onclick="saveManualWeight()">Update Weight</button>
        </div>
    </div>

    <!-- ACHIEVEMENT UNLOCKED POPUP -->
    <div class="achievement-popup" id="achievement-popup-modal">
        <div class="glass-card achievement-popup-card">
            <div class="popup-badge-icon" id="popup-badge-icon-val">🏆</div>
            <div class="popup-title">Milestone Achieved!</div>
            <h3 id="popup-badge-name-val" style="font-size: 20px; font-weight:700; color:#fff;">First Workout</h3>
            <p class="popup-desc" id="popup-badge-desc-val">Log your first exercise session.</p>
            <button class="btn-profile" style="width: auto; padding: 12px 30px; font-size:13px;" onclick="closeAchievementPopup()">Let's Keep Going!</button>
        </div>
        <!-- Internal particles canvas for confetti -->
        <canvas id="confetti-canvas" style="position: absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:-1;"></canvas>
    </div>

    <!-- LOG CUSTOM FOOD MODAL -->
    <div class="modal-overlay" id="log-custom-food-modal">
        <div class="glass-card modal-card">
            <div class="modal-header">
                <div>
                    <div class="modal-food-category">Custom Tracker</div>
                    <div class="modal-food-name">Log Custom Food</div>
                </div>
                <button class="modal-close" onclick="closeCustomFoodModal()">✕</button>
            </div>
            
            <div class="input-group">
                <label for="custom-food-name">Food Name</label>
                <input type="text" id="custom-food-name" placeholder="e.g. Grandma's Apple Pie">
            </div>

            <div class="serving-selector-row">
                <div class="input-group">
                    <label for="custom-food-cal">Calories (kcal)</label>
                    <input type="number" id="custom-food-cal" value="250" min="0" max="10000">
                </div>
                <div class="input-group">
                    <label for="custom-food-prot">Protein (g)</label>
                    <input type="number" id="custom-food-prot" value="5" min="0" max="500" step="0.1">
                </div>
            </div>

            <div class="serving-selector-row">
                <div class="input-group">
                    <label for="custom-food-carb">Carbs (g)</label>
                    <input type="number" id="custom-food-carb" value="30" min="0" max="500" step="0.1">
                </div>
                <div class="input-group">
                    <label for="custom-food-fat">Fat (g)</label>
                    <input type="number" id="custom-food-fat" value="10" min="0" max="500" step="0.1">
                </div>
            </div>

            <div class="serving-selector-row">
                <div class="input-group">
                    <label for="custom-food-serving">Serving Unit</label>
                    <input type="text" id="custom-food-serving" value="1 portion" placeholder="e.g. 1 bowl, 100g">
                </div>
                <div class="input-group">
                    <label for="custom-food-quantity">Quantity</label>
                    <input type="number" id="custom-food-quantity" value="1" min="0.1" max="100" step="0.1">
                </div>
            </div>

            <div class="serving-selector-row">
                <div class="input-group">
                    <label for="custom-food-meal-type">Logged Meal</label>
                    <select id="custom-food-meal-type">
                        <option value="Breakfast">Breakfast</option>
                        <option value="Lunch">Lunch</option>
                        <option value="Dinner">Dinner</option>
                        <option value="Snacks">Snacks</option>
                    </select>
                </div>
                <div class="input-group" style="flex-direction: row; align-items: center; gap: 8px; margin-top: 24px;">
                    <input type="checkbox" id="custom-food-save-db" checked style="width: 18px; height: 18px; cursor: pointer;">
                    <label for="custom-food-save-db" style="cursor: pointer; font-size: 13px;">Save to My Foods list</label>
                </div>
            </div>

            <button class="btn-log-action" onclick="saveCustomFoodLog()">Log Custom Food</button>
        </div>
    </div>

    <script>
        // GLOBALS & STATE
        const FOOD_DB = {foods_json};
        const EXERCISE_DB = {exercises_json};

        let state = {{
            profile: {{
                weight: 70,
                height: 175,
                goalWeight: 65,
                calorieGoal: 2200,
                waterGoal: 3000,
                stepsGoal: 10000,
                sleepGoal: 8
            }},
            history: {{}},
            streaks: {{
                current: 0,
                best: 0,
                lastActiveDate: ""
            }},
            unlockedAchievements: [],
            customFoods: []
        }};

        let activeDateStr = "";
        let activeMealCategory = "Breakfast";
        let activeCardioType = "Walking";
        let activeCardioIcon = "👟";
        let chartPeriodDays = 7;
        let selectedFoodItem = null;

        // Date utilities
        function getTodayString() {{
            const now = new Date();
            const year = now.getFullYear();
            const month = String(now.getMonth() + 1).padStart(2, '0');
            const day = String(now.getDate()).padStart(2, '0');
            return `${{year}}-${{month}}-${{day}}`;
        }}

        function getDaysDifference(d1, d2) {{
            const date1 = new Date(d1);
            const date2 = new Date(d2);
            const diffTime = Math.abs(date2 - date1);
            return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        }}

        // Core data structure template for a fresh day record
        function createFreshDayData() {{
            return {{
                foodLog: [],
                water: 0,
                steps: 0,
                sleep: 0,
                sleepQuality: "Good",
                weight: state.profile.weight,
                note: "",
                cardioLog: [],
                gymLog: []
            }};
        }}

        function getActiveDayData() {{
            if (!state.history[activeDateStr]) {{
                state.history[activeDateStr] = createFreshDayData();
            }}
            return state.history[activeDateStr];
        }}

        // LocalStorage Logic
        function saveState() {{
            // Clean history records older than 365 days
            const keys = Object.keys(state.history).sort();
            while (keys.length > 365) {{
                const oldest = keys.shift();
                delete state.history[oldest];
            }}

            localStorage.setItem("health-tracker", JSON.stringify(state));
            checkAchievements();
            updateUI();
        }}

        function loadState() {{
            const stored = localStorage.getItem("health-tracker");
            if (stored) {{
                try {{
                    const parsed = JSON.parse(stored);
                    state = {{ ...state, ...parsed }};
                }} catch (e) {{
                    console.error("Failed to parse local storage", e);
                }}
            }}

            // Ensure profile is fully populated
            if (!state.profile.weight) state.profile.weight = 70;
            if (!state.profile.height) state.profile.height = 175;
            if (!state.profile.goalWeight) state.profile.goalWeight = 65;
            if (!state.profile.calorieGoal) state.profile.calorieGoal = 2200;
            if (!state.profile.waterGoal) state.profile.waterGoal = 3000;
            if (!state.profile.stepsGoal) state.profile.stepsGoal = 10000;
            if (!state.profile.sleepGoal) state.profile.sleepGoal = 8;
            if (!state.customFoods) state.customFoods = [];

            const todayStr = getTodayString();
            activeDateStr = todayStr;
            document.getElementById('active-date-picker').value = todayStr;

            // Check and update streaks
            updateStreaks();
            
            // Create record for today if absent
            if (!state.history[todayStr]) {{
                state.history[todayStr] = createFreshDayData();
            }}

            updateUI();
        }}

        function updateStreaks() {{
            const todayStr = getTodayString();
            if (state.streaks.lastActiveDate === todayStr) return;

            const lastDate = state.streaks.lastActiveDate;
            if (!lastDate) {{
                state.streaks.current = 1;
                state.streaks.best = 1;
                state.streaks.lastActiveDate = todayStr;
                return;
            }}

            const diff = getDaysDifference(lastDate, todayStr);
            if (diff === 1) {{
                // Check if yesterday was active
                const yesterdayData = state.history[lastDate];
                const wasActive = yesterdayData && (
                    yesterdayData.steps > 0 ||
                    yesterdayData.water > 0 ||
                    yesterdayData.sleep > 0 ||
                    yesterdayData.foodLog.length > 0 ||
                    yesterdayData.gymLog.length > 0 ||
                    yesterdayData.cardioLog.length > 0
                );
                if (wasActive) {{
                    state.streaks.current += 1;
                    if (state.streaks.current > state.streaks.best) {{
                        state.streaks.best = state.streaks.current;
                    }}
                }} else {{
                    state.streaks.current = 1;
                }}
            }} else if (diff > 1) {{
                state.streaks.current = 1;
            }}

            state.streaks.lastActiveDate = todayStr;
        }}

        // NAVIGATION SWITCHER
        function switchTab(tabId) {{
            // Deactivate all
            document.querySelectorAll('.app-tab').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));

            // Activate select
            document.getElementById(`tab-${{tabId}}`).classList.add('active');
            document.getElementById(`nav-${{tabId}}`).classList.add('active');

            if (tabId === 'analytics') {{
                // Force canvas redrawing
                setTimeout(drawAnalyticsChart, 50);
            }}
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        // ANIMATED COUNTER UTILITY
        function animateValue(obj, start, end, duration) {{
            let startTimestamp = null;
            const step = (timestamp) => {{
                if (!startTimestamp) startTimestamp = timestamp;
                const progress = Math.min((timestamp - startTimestamp) / duration, 1);
                const val = Math.floor(progress * (end - start) + start);
                obj.innerText = val;
                if (progress < 1) {{
                    window.requestAnimationFrame(step);
                }} else {{
                    obj.innerText = end;
                }}
            }};
            window.requestAnimationFrame(step);
        }}

        // DYNAMIC RENDERING & UI UPDATES
        function updateUI() {{
            const dayData = getActiveDayData();

            // Calories Math
            const consumed = dayData.foodLog.reduce((sum, item) => sum + item.calories, 0);
            const burnedGym = dayData.gymLog.reduce((sum, item) => sum + item.caloriesBurned, 0);
            const burnedCardio = dayData.cardioLog.reduce((sum, item) => sum + item.calories, 0);
            const burnedTotal = Math.round(burnedGym + burnedCardio);
            const netCalories = Math.round(consumed - burnedTotal);

            // Goals progress
            const calorieGoal = state.profile.calorieGoal;
            const waterGoal = state.profile.waterGoal;
            const stepsGoal = state.profile.stepsGoal;
            const sleepGoal = state.profile.sleepGoal;

            // Macros Math
            const protein = dayData.foodLog.reduce((sum, item) => sum + item.protein, 0);
            const carbs = dayData.foodLog.reduce((sum, item) => sum + item.carbs, 0);
            const fat = dayData.foodLog.reduce((sum, item) => sum + item.fat, 0);

            // Macros goals estimates (standard proportions: 30% P, 40% C, 30% F)
            const proteinGoal = Math.round((calorieGoal * 0.30) / 4);
            const carbsGoal = Math.round((calorieGoal * 0.40) / 4);
            const fatGoal = Math.round((calorieGoal * 0.30) / 9);

            // Update Net Calories dashboard items
            document.getElementById('net-calories-val').innerText = `${{netCalories}} kcal`;
            document.getElementById('calories-goal-text').innerText = `Goal: ${{calorieGoal}} kcal (In: ${{Math.round(consumed)}} | Out: ${{burnedTotal}})`;
            
            // Adjust Calorie Progress bar
            const caloriePercent = Math.min((consumed / calorieGoal) * 100, 100);
            document.getElementById('calories-progress-bar').style.width = `${{caloriePercent}}%`;

            // Update Steps Card
            document.getElementById('steps-val').innerText = dayData.steps.toLocaleString();
            document.getElementById('steps-goal-text').innerText = `Goal: ${{stepsGoal.toLocaleString()}}`;
            const stepsPercent = Math.min((dayData.steps / stepsGoal) * 100, 100);
            document.getElementById('steps-progress-bar').style.width = `${{stepsPercent}}%`;

            // Update Water Card
            document.getElementById('water-val').innerText = `${{dayData.water}} ml`;
            document.getElementById('water-goal-text').innerText = `Goal: ${{waterGoal}} ml`;
            const waterPercent = Math.min((dayData.water / waterGoal) * 100, 100);
            document.getElementById('water-progress-bar').style.width = `${{waterPercent}}%`;

            // Update Sleep Card
            document.getElementById('sleep-val').innerText = `${{dayData.sleep}}h (${{dayData.sleepQuality}})`;
            document.getElementById('sleep-goal-text').innerText = `Goal: ${{sleepGoal}}h`;
            const sleepPercent = Math.min((dayData.sleep / sleepGoal) * 100, 100);
            document.getElementById('sleep-progress-bar').style.width = `${{sleepPercent}}%`;

            // Update Streaks
            document.getElementById('streak-count-val').innerText = state.streaks.current;

            // Macros Display
            document.getElementById('macro-protein-val').innerText = `${{Math.round(protein)}}g / ${{proteinGoal}}g`;
            document.getElementById('macro-carbs-val').innerText = `${{Math.round(carbs)}}g / ${{carbsGoal}}g`;
            document.getElementById('macro-fat-val').innerText = `${{Math.round(fat)}}g / ${{fatGoal}}g`;

            document.getElementById('protein-bar').style.width = `${{Math.min((protein / proteinGoal) * 100, 100)}}%`;
            document.getElementById('carbs-bar').style.width = `${{Math.min((carbs / carbsGoal) * 100, 100)}}%`;
            document.getElementById('fat-bar').style.width = `${{Math.min((fat / fatGoal) * 100, 100)}}%`;

            // Weight & BMI Display
            const heightM = state.profile.height / 100;
            const currentWeight = dayData.weight || state.profile.weight;
            const bmi = (currentWeight / (heightM * heightM)).toFixed(1);
            
            document.getElementById('weight-current-val').innerText = `${{currentWeight}} kg`;
            document.getElementById('weight-goal-val').innerText = `${{state.profile.goalWeight}} kg`;
            document.getElementById('bmi-val').innerText = bmi;

            // BMI Status
            let bmiStatus = "Normal";
            let bmiClass = "bmi-status-badge";
            let bmiBgColor = "rgba(16, 185, 129, 0.15)";
            let bmiTextColor = "#10b981";

            if (bmi < 18.5) {{
                bmiStatus = "Underweight";
                bmiBgColor = "rgba(6, 182, 212, 0.15)";
                bmiTextColor = "#06b6d4";
            }} else if (bmi >= 25 && bmi < 30) {{
                bmiStatus = "Overweight";
                bmiBgColor = "rgba(245, 158, 11, 0.15)";
                bmiTextColor = "#f59e0b";
            }} else if (bmi >= 30) {{
                bmiStatus = "Obese";
                bmiBgColor = "rgba(239, 68, 68, 0.15)";
                bmiTextColor = "#ef4444";
            }}

            const badgeEl = document.getElementById('bmi-badge');
            badgeEl.innerText = bmiStatus;
            badgeEl.style.backgroundColor = bmiBgColor;
            badgeEl.style.color = bmiTextColor;

            // Weight Change
            const weightDiff = (currentWeight - state.profile.goalWeight).toFixed(1);
            let diffText = "";
            if (weightDiff > 0) {{
                diffText = `${{weightDiff}} kg over goal`;
            }} else if (weightDiff < 0) {{
                diffText = `${{Math.abs(weightDiff)}} kg below goal`;
            }} else {{
                diffText = "Target reached!";
            }}
            document.getElementById('weight-diff-text').innerText = diffText;

            // Health Score Math
            let score = 0;
            
            // 1. Calories (20 pts)
            const calDiffPercent = Math.abs(consumed - calorieGoal) / calorieGoal;
            if (consumed > 0) {{
                if (calDiffPercent <= 0.1) score += 20;
                else if (calDiffPercent <= 0.25) score += 15;
                else if (calDiffPercent <= 0.5) score += 10;
                else score += 5;
            }}
            
            // 2. Steps (20 pts)
            score += Math.min(dayData.steps / stepsGoal, 1) * 20;
            
            // 3. Water (20 pts)
            score += Math.min(dayData.water / waterGoal, 1) * 20;
            
            // 4. Sleep (20 pts)
            score += Math.min(dayData.sleep / sleepGoal, 1) * 20;
            
            // 5. Exercise (20 pts)
            const didExercise = (dayData.cardioLog.length > 0 || dayData.gymLog.length > 0);
            if (didExercise) score += 20;

            const finalScore = Math.round(score);
            
            // Animate Health Score ring
            const scoreRing = document.getElementById('score-ring-circle');
            const circumference = 2 * Math.PI * 70; // 439.8
            const strokeOffset = circumference - (finalScore / 100) * circumference;
            scoreRing.style.strokeDashoffset = strokeOffset;
            
            // Animate health score number
            const scoreNumEl = document.getElementById('health-score-val');
            animateValue(scoreNumEl, parseInt(scoreNumEl.innerText) || 0, finalScore, 600);

            // Notes textbox loading
            document.getElementById('daily-notes-input').value = dayData.note || "";

            // Render Tab-specific items
            renderDietView(dayData, consumed);
            renderWorkoutsView(dayData, burnedTotal);
            renderSettingsView();
            renderAICoachFeed(consumed, calorieGoal, dayData.water, waterGoal, dayData.steps, stepsGoal, protein, proteinGoal, dayData.sleep);
        }}

        // DIET LOG VIEW RENDERING
        function renderDietView(dayData, consumedTotal) {{
            const meals = ["Breakfast", "Lunch", "Dinner", "Snacks"];
            meals.forEach(meal => {{
                const listEl = document.getElementById(`${{meal.toLowerCase()}}-items-list`);
                const calText = document.getElementById(`${{meal.toLowerCase()}}-cal-total`);
                
                const mealFoods = dayData.foodLog.filter(item => item.meal === meal);
                const mealCalories = Math.round(mealFoods.reduce((sum, item) => sum + item.calories, 0));
                
                calText.innerText = `${{mealCalories}} kcal`;
                listEl.innerHTML = "";

                if (mealFoods.length === 0) {{
                    listEl.innerHTML = `<div style="font-size: 12px; color: var(--text-muted); text-align: center; padding: 12px;">No logged items</div>`;
                }} else {{
                    mealFoods.forEach(item => {{
                        const row = document.createElement('div');
                        row.className = "meal-item-row";
                        row.innerHTML = `
                            <div class="meal-item-info">
                                <div class="meal-item-name">${{item.name}}</div>
                                <div class="meal-item-sub">${{item.quantity}}x ${{item.serving}} | P: ${{Math.round(item.protein)}}g C: ${{Math.round(item.carbs)}}g F: ${{Math.round(item.fat)}}g</div>
                            </div>
                            <div class="d-flex align-center gap-12">
                                <span style="font-size: 13.5px; font-weight: 700; color: #ff5e62;">${{Math.round(item.calories)}} kcal</span>
                                <button class="meal-item-delete" onclick="deleteLoggedFood('${{item.id}}')">✕</button>
                            </div>
                        `;
                        listEl.appendChild(row);
                    }});
                }}
            }});

            // Render Hydration tab items
            const waterPercent = Math.min((dayData.water / state.profile.waterGoal) * 100, 100);
            const waterOffset = 377 - (waterPercent / 100) * 377;
            document.getElementById('water-ring-circle').style.strokeDashoffset = waterOffset;
            document.getElementById('water-tab-val').innerText = `${{dayData.water}} ml`;
            document.getElementById('water-tab-goal-text').innerText = `of ${{ (state.profile.waterGoal / 1000).toFixed(1) }}L`;
        }}

        // WORKOUTS VIEW RENDERING
        function renderWorkoutsView(dayData, burnedTotal) {{
            document.getElementById('workouts-burned-total').innerText = `${{burnedTotal}} kcal burned`;
            const listEl = document.getElementById('logged-workouts-list');
            listEl.innerHTML = "";

            const combinedLog = [];
            
            // Add gym sessions
            dayData.gymLog.forEach((item, idx) => {{
                combinedLog.push({{
                    id: `gym-${{idx}}`,
                    type: "resistance",
                    name: item.exercise,
                    details: `${{item.sets}} sets x ${{item.reps}} reps | ${{item.weight}} kg`,
                    calories: item.caloriesBurned,
                    rawIndex: idx
                }});
            }});

            // Add cardio sessions
            dayData.cardioLog.forEach((item, idx) => {{
                combinedLog.push({{
                    id: `cardio-${{idx}}`,
                    type: "cardio",
                    name: item.type,
                    details: item.distance ? `${{item.distance}} km | ${{item.duration}} mins` : `${{item.duration}} mins`,
                    calories: item.calories,
                    rawIndex: idx
                }});
            }});

            if (combinedLog.length === 0) {{
                listEl.innerHTML = `<div style="font-size: 13px; color: var(--text-secondary); text-align:center; padding: 24px;">No activities logged for today. Start moving!</div>`;
            }} else {{
                combinedLog.forEach(item => {{
                    const el = document.createElement('div');
                    el.className = "workout-history-item";
                    el.innerHTML = `
                        <div class="workout-history-info">
                            <div class="workout-history-name">${{item.name}}</div>
                            <div class="workout-history-details">${{item.details}}</div>
                        </div>
                        <div class="d-flex align-center gap-12">
                            <span class="workout-history-calories">-${{Math.round(item.calories)}} kcal</span>
                            <button class="meal-item-delete" onclick="deleteLoggedWorkout('${{item.type}}', ${{item.rawIndex}})">✕</button>
                        </div>
                    `;
                    listEl.appendChild(el);
                }});
            }}
        }}

        // SETTINGS & PROFILE CONFIG RENDERING
        function renderSettingsView() {{
            document.getElementById('profile-height').value = state.profile.height;
            document.getElementById('profile-weight').value = state.profile.weight;
            document.getElementById('profile-goal-weight').value = state.profile.goalWeight;
            
            document.getElementById('profile-calories').value = state.profile.calorieGoal;
            document.getElementById('profile-water').value = state.profile.waterGoal;
            document.getElementById('profile-steps').value = state.profile.stepsGoal;
            document.getElementById('profile-sleep').value = state.profile.sleepGoal;

            // Load achievements gallery status
            const badgeCount = state.unlockedAchievements.length;
            document.getElementById('unlocked-badge-count').innerText = `${{badgeCount}}/11 Unlocked`;

            const badgeGrid = document.getElementById('achievements-gallery-grid');
            badgeGrid.innerHTML = "";

            const badges = {{
                first_workout: {{ name: "First Sweat", desc: "Log your first workout session", icon: "💪" }},
                workouts_10: {{ name: "Consistent Athlete", desc: "Log 10 workouts across history", icon: "🏋️‍♂️" }},
                workouts_50: {{ name: "Iron Warrior", desc: "Log 50 workouts across history", icon: "🔥" }},
                workouts_100: {{ name: "Elite Performer", desc: "Log 100 workouts across history", icon: "👑" }},
                steps_10k: {{ name: "10k Milestone", desc: "Walk 10,000 steps in a single day", icon: "🚶" }},
                steps_100k: {{ name: "Centurion Walker", desc: "Walk a total of 100,000 steps across history", icon: "🏃" }},
                water_master: {{ name: "Water Master", desc: "Meet your daily hydration goal", icon: "💧" }},
                sleep_champion: {{ name: "Sleep Champion", desc: "Log 8+ hours of sleep in a single day", icon: "😴" }},
                streak_7: {{ name: "7-Day Streak", desc: "Maintain a 7-day streak", icon: "⚡" }},
                streak_30: {{ name: "30-Day Streak", desc: "Maintain a 30-day streak", icon: "🔥" }},
                streak_90: {{ name: "90-Day Streak", desc: "Maintain a 90-day streak", icon: "🛡️" }}
            }};

            Object.keys(badges).forEach(key => {{
                const badge = badges[key];
                const isUnlocked = state.unlockedAchievements.includes(key);
                
                const item = document.createElement('div');
                item.className = `achievement-badge ${{isUnlocked ? 'unlocked' : ''}}`;
                item.onclick = () => alert(`${{badge.name}}: ${{badge.desc}} (${{isUnlocked ? 'Unlocked' : 'Locked'}}).`);
                item.innerHTML = `
                    <div class="badge-icon-holder">${{badge.icon}}</div>
                    <div class="badge-label">${{badge.name}}</div>
                `;
                badgeGrid.appendChild(item);
            }});
        }}

        function saveProfileSettings() {{
            state.profile.height = parseInt(document.getElementById('profile-height').value) || 175;
            state.profile.weight = parseInt(document.getElementById('profile-weight').value) || 70;
            state.profile.goalWeight = parseInt(document.getElementById('profile-goal-weight').value) || 65;
            state.profile.calorieGoal = parseInt(document.getElementById('profile-calories').value) || 2200;
            state.profile.waterGoal = parseInt(document.getElementById('profile-water').value) || 3000;
            state.profile.stepsGoal = parseInt(document.getElementById('profile-steps').value) || 10000;
            state.profile.sleepGoal = parseFloat(document.getElementById('profile-sleep').value) || 8;

            saveState();
        }}

        // AI COACHING ENGINE
        function renderAICoachFeed(consumed, calGoal, water, waterGoal, steps, stepsGoal, protein, proteinGoal, sleep) {{
            const feed = document.getElementById('coach-tips-feed');
            feed.innerHTML = "";

            const tips = [];

            // 1. Water Guidance
            if (water < waterGoal) {{
                const rem = ((waterGoal - water) / 1000).toFixed(1);
                tips.push({{
                    icon: "💧",
                    text: `Drink ${{rem}}L more water to hit your hydration target.`
                }});
            }} else {{
                tips.push({{
                    icon: "✅",
                    text: "Hydration target achieved! Keep it up."
                }});
            }}

            // 2. Steps Guidance
            if (steps < stepsGoal) {{
                const rem = stepsGoal - steps;
                tips.push({{
                    icon: "🏃",
                    text: `You need ${{rem.toLocaleString()}} more steps. A quick walk would bridge the gap.`
                }});
            }} else {{
                tips.push({{
                    icon: "🎉",
                    text: "Steps milestone achieved! Excellent activity level today."
                }});
            }}

            // 3. Protein Guidance
            if (protein < proteinGoal) {{
                tips.push({{
                    icon: "🍗",
                    text: `Protein intake is a bit low (${{Math.round(protein)}}g). Try chicken breast, eggs, or paneer.`
                }});
            }} else {{
                tips.push({{
                    icon: "💪",
                    text: "Protein goals hit! Optimal recovery metrics."
                }});
            }}

            // 4. Sleep Guidance
            if (sleep < 7) {{
                tips.push({{
                    icon: "😴",
                    text: "Aim for at least 7-8 hours of sleep tonight to boost physical recovery."
                }});
            }}

            // 5. Streaks Motivation
            if (state.streaks.current >= 3) {{
                tips.push({{
                    icon: "⚡",
                    text: `Impressive streak! You have stayed consistent for ${{state.streaks.current}} consecutive days.`
                }});
            }}

            // Take up to 4 tips to show
            tips.slice(0, 4).forEach(tip => {{
                const el = document.createElement('div');
                el.className = "coach-tip-item";
                el.innerHTML = `
                    <span class="coach-tip-icon">${{tip.icon}}</span>
                    <div>${{tip.text}}</div>
                `;
                feed.appendChild(el);
            }});
        }}

        // FOOD DATABASE SEARCH & FILTERING
        function initFoodDatabase() {{
            // Load Category Pills
            const categories = [
                "All", "My Foods", "Indian Foods", "Fruits", "Vegetables", "Dairy", "Meat", 
                "Seafood", "Fast Food", "Drinks", "Snacks", "Protein Foods", 
                "Breakfast Foods", "Restaurant Foods"
            ];
            const filterContainer = document.getElementById('food-category-filters');
            filterContainer.innerHTML = "";

            categories.forEach((cat, idx) => {{
                const pill = document.createElement('div');
                pill.className = `filter-pill ${{idx === 0 ? 'active' : ''}}`;
                pill.innerText = cat;
                pill.onclick = () => {{
                    document.querySelectorAll('.filter-pill').forEach(p => p.classList.remove('active'));
                    pill.classList.add('active');
                    filterFoods();
                }};
                filterContainer.appendChild(pill);
            }});

            // Bind search keyup
            document.getElementById('food-search-input').oninput = filterFoods;

            // Load initial list
            filterFoods();
        }}

        function filterFoods() {{
            const search = document.getElementById('food-search-input').value.toLowerCase();
            const activePill = document.querySelector('.filter-pill.active');
            const category = activePill ? activePill.innerText : "All";
            const resultsContainer = document.getElementById('food-search-results');
            resultsContainer.innerHTML = "";

            const allFoods = [...FOOD_DB, ...(state.customFoods || [])];
            const filtered = allFoods.filter(food => {{
                const matchSearch = food.name.toLowerCase().includes(search);
                const matchCategory = (category === "All") || (food.category === category);
                return matchSearch && matchCategory;
            }});

            // Display top 50 items for speed
            const limit = 50;
            const slice = filtered.slice(0, limit);

            slice.forEach(food => {{
                const item = document.createElement('div');
                item.className = "search-result-item";
                item.onclick = () => openFoodModal(food);
                item.innerHTML = `
                    <div class="search-result-info">
                        <span class="search-result-name">${{food.name}}</span>
                        <span class="search-result-sub">Category: ${{food.category}} | Unit: ${{food.serving}}</span>
                    </div>
                    <span class="search-result-macros">${{Math.round(food.calories)}} kcal</span>
                `;
                resultsContainer.appendChild(item);
            }});

            if (filtered.length === 0) {{
                resultsContainer.innerHTML = `<div style="font-size: 13px; color: var(--text-muted); text-align: center; padding: 24px;">No items match search...</div>`;
            }}
        }}

        // FOOD LOG DIALOG / MODAL
        function openFoodSearch(mealCategory) {{
            activeMealCategory = mealCategory;
            switchTab('diet');
            document.getElementById('food-search-input').focus();
        }}

        function openFoodModal(food) {{
            selectedFoodItem = food;
            document.getElementById('modal-item-category').innerText = food.category;
            document.getElementById('modal-item-name').innerText = food.name;
            document.getElementById('modal-quantity').value = "1";
            document.getElementById('modal-meal-type').value = activeMealCategory;

            // Load serving sizes options
            const selectUnit = document.getElementById('modal-serving-size');
            selectUnit.innerHTML = "";

            // Standard units
            const baseUnit = food.serving; // e.g. "100g", "1 piece", "1 cup"
            const opt1 = document.createElement('option');
            opt1.value = "1";
            opt1.innerText = baseUnit;
            selectUnit.appendChild(opt1);

            // Add standard alternate units if grams are present
            if (baseUnit.includes("100g") || baseUnit.includes("g")) {{
                const opt2 = document.createElement('option');
                opt2.value = "0.01";
                opt2.innerText = "1g";
                selectUnit.appendChild(opt2);
            }}

            calculateModalMacros();
            document.getElementById('log-food-modal').style.display = 'flex';
        }}

        function closeFoodModal() {{
            document.getElementById('log-food-modal').style.display = 'none';
        }}

        function openCustomFoodModal() {{
            document.getElementById('custom-food-name').value = "";
            document.getElementById('custom-food-cal').value = "250";
            document.getElementById('custom-food-prot').value = "5";
            document.getElementById('custom-food-carb').value = "30";
            document.getElementById('custom-food-fat').value = "10";
            document.getElementById('custom-food-serving').value = "1 portion";
            document.getElementById('custom-food-quantity').value = "1";
            document.getElementById('custom-food-meal-type').value = activeMealCategory;
            document.getElementById('custom-food-save-db').checked = true;
            document.getElementById('log-custom-food-modal').style.display = 'flex';
        }}

        function closeCustomFoodModal() {{
            document.getElementById('log-custom-food-modal').style.display = 'none';
        }}

        function saveCustomFoodLog() {{
            const name = document.getElementById('custom-food-name').value.trim() || "Custom Food Item";
            const cal = parseFloat(document.getElementById('custom-food-cal').value) || 0;
            const prot = parseFloat(document.getElementById('custom-food-prot').value) || 0;
            const carb = parseFloat(document.getElementById('custom-food-carb').value) || 0;
            const fat = parseFloat(document.getElementById('custom-food-fat').value) || 0;
            const serving = document.getElementById('custom-food-serving').value.trim() || "1 portion";
            const quantity = parseFloat(document.getElementById('custom-food-quantity').value) || 1;
            const meal = document.getElementById('custom-food-meal-type').value;
            const saveToDb = document.getElementById('custom-food-save-db').checked;

            const dayData = getActiveDayData();

            dayData.foodLog.push({{
                id: Math.random().toString(36).substr(2, 9),
                name: name,
                meal: meal,
                quantity: quantity,
                serving: serving,
                calories: cal * quantity,
                protein: prot * quantity,
                carbs: carb * quantity,
                fat: fat * quantity
            }});

            if (saveToDb) {{
                if (!state.customFoods) state.customFoods = [];
                const exists = state.customFoods.some(f => f.name.toLowerCase() === name.toLowerCase());
                if (!exists) {{
                    state.customFoods.push({{
                        name: name,
                        category: "My Foods",
                        serving: serving,
                        calories: cal,
                        protein: prot,
                        carbs: carb,
                        fat: fat
                    }});
                }}
            }}

            closeCustomFoodModal();
            saveState();
            filterFoods();
        }}

        function calculateModalMacros() {{
            if (!selectedFoodItem) return;
            const q = parseFloat(document.getElementById('modal-quantity').value) || 0;
            const u = parseFloat(document.getElementById('modal-serving-size').value) || 1;

            const multiplier = q * u;

            const cal = Math.round(selectedFoodItem.calories * multiplier);
            const prot = (selectedFoodItem.protein * multiplier).toFixed(1);
            const carb = (selectedFoodItem.carbs * multiplier).toFixed(1);
            const fat = (selectedFoodItem.fat * multiplier).toFixed(1);

            document.getElementById('modal-preview-cal').innerText = cal;
            document.getElementById('modal-preview-prot').innerText = `${{prot}}g`;
            document.getElementById('modal-preview-carb').innerText = `${{carb}}g`;
            document.getElementById('modal-preview-fat').innerText = `${{fat}}g`;
        }}

        function addFoodToLog() {{
            if (!selectedFoodItem) return;
            const q = parseFloat(document.getElementById('modal-quantity').value) || 1;
            const u = parseFloat(document.getElementById('modal-serving-size').value) || 1;
            const meal = document.getElementById('modal-meal-type').value;

            const multiplier = q * u;
            const dayData = getActiveDayData();

            dayData.foodLog.push({{
                id: Math.random().toString(36).substr(2, 9),
                name: selectedFoodItem.name,
                meal: meal,
                quantity: q,
                serving: document.getElementById('modal-serving-size').options[document.getElementById('modal-serving-size').selectedIndex].text,
                calories: selectedFoodItem.calories * multiplier,
                protein: selectedFoodItem.protein * multiplier,
                carbs: selectedFoodItem.carbs * multiplier,
                fat: selectedFoodItem.fat * multiplier
            }});

            closeFoodModal();
            saveState();
        }}

        function deleteLoggedFood(id) {{
            const dayData = getActiveDayData();
            dayData.foodLog = dayData.foodLog.filter(item => item.id !== id);
            saveState();
        }}

        // WATER ACTIONS
        function addWater(amount) {{
            const dayData = getActiveDayData();
            dayData.water += amount;
            saveState();
        }}

        // MANUAL LOGGERS
        function openStepsLogger() {{
            const dayData = getActiveDayData();
            document.getElementById('manual-steps-input').value = dayData.steps;
            document.getElementById('log-steps-modal').style.display = 'flex';
        }}
        function closeStepsLogger() {{
            document.getElementById('log-steps-modal').style.display = 'none';
        }}
        function saveManualSteps() {{
            const dayData = getActiveDayData();
            dayData.steps = parseInt(document.getElementById('manual-steps-input').value) || 0;
            closeStepsLogger();
            saveState();
        }}

        function openSleepLogger() {{
            const dayData = getActiveDayData();
            document.getElementById('manual-sleep-hours').value = dayData.sleep || 8;
            document.getElementById('manual-sleep-quality').value = dayData.sleepQuality || "Good";
            document.getElementById('log-sleep-modal').style.display = 'flex';
        }}
        function closeSleepLogger() {{
            document.getElementById('log-sleep-modal').style.display = 'none';
        }}
        function saveManualSleep() {{
            const dayData = getActiveDayData();
            dayData.sleep = parseFloat(document.getElementById('manual-sleep-hours').value) || 0;
            dayData.sleepQuality = document.getElementById('manual-sleep-quality').value;
            closeSleepLogger();
            saveState();
        }}

        function openWeightLogger() {{
            const dayData = getActiveDayData();
            document.getElementById('manual-weight-input').value = dayData.weight || state.profile.weight;
            document.getElementById('log-weight-modal').style.display = 'flex';
        }}
        function closeWeightLogger() {{
            document.getElementById('log-weight-modal').style.display = 'none';
        }}
        function saveManualWeight() {{
            const dayData = getActiveDayData();
            const w = parseFloat(document.getElementById('manual-weight-input').value) || state.profile.weight;
            dayData.weight = w;
            state.profile.weight = w; // update default profile weight too
            closeWeightLogger();
            saveState();
        }}

        // WORKOUT LOGGERS
        function toggleWorkoutType(type) {{
            document.querySelectorAll('.workout-pill').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.workout-panel').forEach(el => el.classList.remove('active'));

            document.getElementById(`pill-${{type}}`).classList.add('active');
            document.getElementById(`panel-${{type}}`).classList.add('active');
        }}

        function initGymExercises() {{
            // Populate muscle groups
            const muscleSelect = document.getElementById('gym-muscle-select');
            filterGymExercises();
        }}

        function filterGymExercises() {{
            const muscle = document.getElementById('gym-muscle-select').value;
            const exSelect = document.getElementById('gym-exercise-select');
            exSelect.innerHTML = "";

            const filtered = EXERCISE_DB.filter(ex => ex.category === muscle);
            filtered.forEach(ex => {{
                const opt = document.createElement('option');
                opt.value = ex.name;
                opt.innerText = ex.name;
                exSelect.appendChild(opt);
            }});
        }}

        function selectCardio(type, icon) {{
            activeCardioType = type;
            activeCardioIcon = icon;
            document.querySelectorAll('.cardio-btn').forEach(btn => btn.classList.remove('active'));
            
            // Find active element
            event.currentTarget.classList.add('active');
            renderCardioFields();
        }}

        function renderCardioFields() {{
            const container = document.getElementById('cardio-fields-container');
            container.innerHTML = "";

            // Walking, Running, Cycling require Distance and Duration
            // Swimming, Yoga, Sports require Duration & Intensity
            const needDistance = ["Walking", "Running", "Cycling"].includes(activeCardioType);

            if (needDistance) {{
                container.innerHTML = `
                    <div class="input-group">
                        <label for="cardio-dist">Distance (km)</label>
                        <input type="number" id="cardio-dist" value="5" min="0.1" max="100" step="0.1">
                    </div>
                    <div class="input-group">
                        <label for="cardio-dur">Duration (minutes)</label>
                        <input type="number" id="cardio-dur" value="30" min="1" max="300">
                    </div>
                `;
            }} else {{
                container.innerHTML = `
                    <div class="input-group">
                        <label for="cardio-dur">Duration (minutes)</label>
                        <input type="number" id="cardio-dur" value="45" min="1" max="300">
                    </div>
                    <div class="input-group">
                        <label for="cardio-intensity">Intensity</label>
                        <select id="cardio-intensity">
                            <option value="Low">Low Effort</option>
                            <option value="Medium" selected>Medium Effort</option>
                            <option value="High">High Effort (Vigorous)</option>
                        </select>
                    </div>
                `;
            }}
        }}

        function logCardioSession() {{
            const dayData = getActiveDayData();
            const w = dayData.weight || state.profile.weight;
            
            let calories = 0;
            let distance = null;
            let duration = 30;

            const isDistanceBased = ["Walking", "Running", "Cycling"].includes(activeCardioType);

            if (isDistanceBased) {{
                distance = parseFloat(document.getElementById('cardio-dist').value) || 0;
                duration = parseFloat(document.getElementById('cardio-dur').value) || 30;
                
                // Formulas for cardio METs
                let met = 3.5; // walking
                if (activeCardioType === "Running") met = 9.8;
                if (activeCardioType === "Cycling") met = 7.5;
                
                calories = met * w * (duration / 60);
            }} else {{
                duration = parseFloat(document.getElementById('cardio-dur').value) || 30;
                const intensity = document.getElementById('cardio-intensity').value;
                
                let baseMet = 5.0;
                if (activeCardioType === "Yoga") baseMet = 2.5;
                if (activeCardioType === "Swimming") baseMet = 8.0;
                if (activeCardioType === "Sports") baseMet = 7.0;

                if (intensity === "Low") baseMet *= 0.7;
                if (intensity === "High") baseMet *= 1.3;

                calories = baseMet * w * (duration / 60);
            }}

            dayData.cardioLog.push({{
                type: activeCardioType,
                distance: distance,
                duration: duration,
                calories: calories
            }});

            // Auto increment steps if Walking/Running is logged and steps = 0
            if (activeCardioType === "Walking" && distance && dayData.steps === 0) {{
                dayData.steps = Math.round(distance * 1300); // 1300 steps per km average
            }} else if (activeCardioType === "Running" && distance && dayData.steps === 0) {{
                dayData.steps = Math.round(distance * 1000); // 1000 steps per km average running
            }}

            saveState();
        }}

        function logGymWorkout() {{
            const dayData = getActiveDayData();
            const exName = document.getElementById('gym-exercise-select').value;
            const muscle = document.getElementById('gym-muscle-select').value;
            const sets = parseInt(document.getElementById('gym-sets').value) || 4;
            const reps = parseInt(document.getElementById('gym-reps').value) || 10;
            const weight = parseInt(document.getElementById('gym-weight').value) || 40;
            const duration = parseFloat(document.getElementById('gym-duration').value) || 30;

            // Resistance MET standard = 5.0
            const w = dayData.weight || state.profile.weight;
            const calories = 5.0 * w * (duration / 60);

            dayData.gymLog.push({{
                exercise: exName,
                muscle: muscle,
                sets: sets,
                reps: reps,
                weight: weight,
                duration: duration,
                caloriesBurned: calories
            }});

            saveState();
        }}

        function deleteLoggedWorkout(type, idx) {{
            const dayData = getActiveDayData();
            if (type === "resistance") {{
                dayData.gymLog.splice(idx, 1);
            }} else {{
                dayData.cardioLog.splice(idx, 1);
            }}
            saveState();
        }}

        // ACHIEVEMENT POPUPS & CHECKING
        function checkAchievements() {{
            const unlocked = [...state.unlockedAchievements];
            const historyKeys = Object.keys(state.history);

            // Compute cumulative totals
            let totalWorkouts = 0;
            let totalSteps = 0;
            let maxStepsSingleDay = 0;

            historyKeys.forEach(k => {{
                const d = state.history[k];
                totalWorkouts += (d.gymLog ? d.gymLog.length : 0) + (d.cardioLog ? d.cardioLog.length : 0);
                totalSteps += d.steps || 0;
                if ((d.steps || 0) > maxStepsSingleDay) {{
                    maxStepsSingleDay = d.steps || 0;
                }}
            }});

            const todayData = getActiveDayData();

            // 1. First Workout
            if (totalWorkouts >= 1 && !unlocked.includes("first_workout")) unlockBadge("first_workout");
            // 2. 10 Workouts
            if (totalWorkouts >= 10 && !unlocked.includes("workouts_10")) unlockBadge("workouts_10");
            // 3. 50 Workouts
            if (totalWorkouts >= 50 && !unlocked.includes("workouts_50")) unlockBadge("workouts_50");
            // 4. 100 Workouts
            if (totalWorkouts >= 100 && !unlocked.includes("workouts_100")) unlockBadge("workouts_100");
            // 5. 10k Steps Single Day
            if (maxStepsSingleDay >= 10000 && !unlocked.includes("steps_10k")) unlockBadge("steps_10k");
            // 6. 100k Steps total
            if (totalSteps >= 100000 && !unlocked.includes("steps_100k")) unlockBadge("steps_100k");
            // 7. Water Master
            if (todayData.water >= state.profile.waterGoal && !unlocked.includes("water_master")) unlockBadge("water_master");
            // 8. Sleep Champion
            if (todayData.sleep >= 8 && !unlocked.includes("sleep_champion")) unlockBadge("sleep_champion");
            // 9. Streaks
            if (state.streaks.current >= 7 && !unlocked.includes("streak_7")) unlockBadge("streak_7");
            if (state.streaks.current >= 30 && !unlocked.includes("streak_30")) unlockBadge("streak_30");
            if (state.streaks.current >= 90 && !unlocked.includes("streak_90")) unlockBadge("streak_90");
        }}

        function unlockBadge(badgeId) {{
            state.unlockedAchievements.push(badgeId);
            showAchievementPopup(badgeId);
        }}

        function showAchievementPopup(badgeId) {{
            const badges = {{
                first_workout: {{ name: "First Sweat", desc: "You've taken the first step on your physical fitness journey by logging a workout session!", icon: "💪" }},
                workouts_10: {{ name: "Consistent Athlete", desc: "Fantastic dedication! You have successfully logged 10 workouts.", icon: "🏋️‍♂️" }},
                workouts_50: {{ name: "Iron Warrior", desc: "Incredible resilience! 50 logged workouts completed.", icon: "🔥" }},
                workouts_100: {{ name: "Elite Performer", desc: "Legendary status reached! 100 workouts completed. You are unstoppable!", icon: "👑" }},
                steps_10k: {{ name: "10k Milestone", desc: "You crushed 10,000 steps in a single day! Keep moving.", icon: "🚶" }},
                steps_100k: {{ name: "Centurion Walker", desc: "A colossal milestone: You have completed 100,000 steps total!", icon: "🏃" }},
                water_master: {{ name: "Water Master", desc: "Perfect hydration logged! Your kidneys thank you.", icon: "💧" }},
                sleep_champion: {{ name: "Sleep Champion", desc: "Optimal sleep recovery! 8+ hours of rest achieved.", icon: "😴" }},
                streak_7: {{ name: "7-Day Streak", desc: "A full week of non-stop daily updates! Incredible streak.", icon: "⚡" }},
                streak_30: {{ name: "30-Day Streak", desc: "One whole month of fitness tracking consistency. Superb discipline!", icon: "🔥" }},
                streak_90: {{ name: "90-Day Streak", desc: "90 days of active dedication. You've officially built a life-changing habit!", icon: "🛡️" }}
            }};

            const b = badges[badgeId];
            if (!b) return;

            document.getElementById('popup-badge-icon-val').innerText = b.icon;
            document.getElementById('popup-badge-name-val').innerText = b.name;
            document.getElementById('popup-badge-desc-val').innerText = b.desc;
            
            document.getElementById('achievement-popup-modal').style.display = 'flex';
            startConfetti();
        }}

        function closeAchievementPopup() {{
            document.getElementById('achievement-popup-modal').style.display = 'none';
            stopConfetti();
        }}

        // Canvas Confetti Particles
        let confettiInterval = null;
        function startConfetti() {{
            const canvas = document.getElementById('confetti-canvas');
            const ctx = canvas.getContext('2d');
            
            canvas.width = canvas.parentElement.clientWidth;
            canvas.height = canvas.parentElement.clientHeight;

            const colors = ["#ff5e62", "#ff9966", "#06b6d4", "#10b981", "#a78bfa", "#f59e0b"];
            const particles = [];

            for (let i = 0; i < 120; i++) {{
                particles.push({{
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height - canvas.height,
                    r: Math.random() * 6 + 4,
                    d: Math.random() * canvas.height,
                    color: colors[Math.floor(Math.random() * colors.length)],
                    tilt: Math.random() * 10 - 5,
                    tiltAngleIncremental: Math.random() * 0.07 + 0.02,
                    tiltAngle: 0
                }});
            }}

            function draw() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                particles.forEach((p, idx) => {{
                    p.tiltAngle += p.tiltAngleIncremental;
                    p.y += (Math.cos(p.d) + 3 + p.r / 2) / 2;
                    p.x += Math.sin(p.tiltAngle);
                    p.tilt = Math.sin(p.tiltAngle - idx / 3) * 15;

                    if (p.y > canvas.height) {{
                        particles[idx] = {{
                            x: Math.random() * canvas.width,
                            y: -20,
                            r: p.r,
                            d: p.d,
                            color: p.color,
                            tilt: p.tilt,
                            tiltAngleIncremental: p.tiltAngleIncremental,
                            tiltAngle: p.tiltAngle
                        }};
                    }}

                    ctx.beginPath();
                    ctx.lineWidth = p.r;
                    ctx.strokeStyle = p.color;
                    ctx.moveTo(p.x + p.tilt + p.r / 2, p.y);
                    ctx.lineTo(p.x + p.tilt, p.y + p.tilt + p.r / 2);
                    ctx.stroke();
                }});
            }}

            confettiInterval = setInterval(draw, 24);
        }}

        function stopConfetti() {{
            if (confettiInterval) {{
                clearInterval(confettiInterval);
                confettiInterval = null;
            }}
        }}

        // BACKUP & RESTORE DATA
        function exportBackupData() {{
            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(state, null, 2));
            const dlAnchorElem = document.createElement('a');
            dlAnchorElem.setAttribute("href",     dataStr     );
            dlAnchorElem.setAttribute("download", `syncfit-backup-${{getTodayString()}}.json`);
            dlAnchorElem.click();
        }}

        function importBackupData(event) {{
            const file = event.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function(e) {{
                try {{
                    const imported = JSON.parse(e.target.result);
                    if (imported.profile && imported.history) {{
                        state = imported;
                        saveState();
                        alert("Database restored successfully!");
                        location.reload();
                    }} else {{
                        alert("Invalid backup file layout.");
                    }}
                }} catch (err) {{
                    alert("Failed to parse JSON backup.");
                }}
            }};
            reader.readAsText(file);
        }}

        function resetAllTrackerData() {{
            if (confirm("WARNING! This will permanently delete all logged history, streaks, and targets. Do you want to continue?")) {{
                localStorage.removeItem("health-tracker");
                alert("Database wiped. App reloading...");
                location.reload();
            }}
        }}

        // ANALYTICS CANVAS DRAWING ENGINE
        function setChartPeriod(days) {{
            chartPeriodDays = days;
            document.querySelectorAll('#chart-period-container .chart-selector-pill').forEach((pill, idx) => {{
                pill.classList.remove('active');
                if ((days === 7 && idx === 0) || (days === 30 && idx === 1) || (days === 90 && idx === 2)) {{
                    pill.classList.add('active');
                }}
            }});
            drawAnalyticsChart();
        }}

        // Custom Mouse Tracker for canvas tooltips
        let canvasHoverIndex = -1;
        function initChartCanvasEvents() {{
            const canvas = document.getElementById('analytics-canvas');
            canvas.addEventListener('mousemove', (e) => {{
                const rect = canvas.getBoundingClientRect();
                const mouseX = e.clientX - rect.left;
                
                // Draw chart with vertical tracker line at mouse
                drawAnalyticsChart(mouseX);
            }});

            canvas.addEventListener('mouseleave', () => {{
                canvasHoverIndex = -1;
                drawAnalyticsChart();
            }});
        }}

        function drawAnalyticsChart(mouseX = -1) {{
            const canvas = document.getElementById('analytics-canvas');
            const ctx = canvas.getContext('2d');

            // Set dynamic canvas resolutions to fit bounding sizes
            const width = canvas.parentElement.clientWidth;
            const height = canvas.parentElement.clientHeight;
            
            // Adjust scaling factors for High DPI displays
            const dpr = window.devicePixelRatio || 1;
            canvas.width = width * dpr;
            canvas.height = height * dpr;
            ctx.scale(dpr, dpr);

            const padding = {{ top: 40, right: 30, bottom: 40, left: 50 }};
            const graphWidth = width - padding.left - padding.right;
            const graphHeight = height - padding.top - padding.bottom;

            const metric = document.getElementById('chart-metric-dropdown').value;
            const dataPoints = [];
            const dates = [];

            // Compile past dates for intervals
            const today = new Date();
            for (let i = chartPeriodDays - 1; i >= 0; i--) {{
                const d = new Date();
                d.setDate(today.getDate() - i);
                const year = d.getFullYear();
                const month = String(d.getMonth() + 1).padStart(2, '0');
                const day = String(d.getDate()).padStart(2, '0');
                const key = `${{year}}-${{month}}-${{day}}`;
                
                dates.push(key);

                // Fetch database metrics
                const record = state.history[key];
                let value = 0;

                if (metric === "Weight") {{
                    value = record ? (record.weight || state.profile.weight) : state.profile.weight;
                }} else if (metric === "Calories") {{
                    const cons = record ? record.foodLog.reduce((s, item) => s + item.calories, 0) : 0;
                    const burnGym = record ? record.gymLog.reduce((s, item) => s + item.caloriesBurned, 0) : 0;
                    const burnCardio = record ? record.cardioLog.reduce((s, item) => s + item.calories, 0) : 0;
                    value = Math.round(cons - (burnGym + burnCardio));
                }} else if (metric === "Burned") {{
                    const burnGym = record ? record.gymLog.reduce((s, item) => s + item.caloriesBurned, 0) : 0;
                    const burnCardio = record ? record.cardioLog.reduce((s, item) => s + item.calories, 0) : 0;
                    value = Math.round(burnGym + burnCardio);
                }} else if (metric === "Protein") {{
                    value = record ? record.foodLog.reduce((s, item) => s + item.protein, 0) : 0;
                }} else if (metric === "Water") {{
                    value = record ? record.water : 0;
                }} else if (metric === "Steps") {{
                    value = record ? record.steps : 0;
                }} else if (metric === "Sleep") {{
                    value = record ? record.sleep : 0;
                }}

                dataPoints.push(value);
            }}

            // Math ranges
            const maxVal = Math.max(...dataPoints, 10);
            const minVal = metric === "Weight" ? Math.min(...dataPoints, state.profile.goalWeight) - 2 : 0;
            const range = maxVal - minVal;

            // Clear canvas background
            ctx.clearRect(0, 0, width, height);

            // Draw Y-Axis grids & marks
            ctx.strokeStyle = "rgba(255, 255, 255, 0.03)";
            ctx.lineWidth = 1;
            ctx.fillStyle = "#8e90a6";
            ctx.font = "11px -apple-system, BlinkMacSystemFont, Segoe UI";
            ctx.textAlign = "right";

            const grids = 4;
            for (let i = 0; i <= grids; i++) {{
                const yVal = minVal + (range / grids) * i;
                const yPos = padding.top + graphHeight - (graphHeight / grids) * i;
                
                // Grid line
                ctx.beginPath();
                ctx.moveTo(padding.left, yPos);
                ctx.lineTo(width - padding.right, yPos);
                ctx.stroke();

                // Y values label
                let formatVal = Math.round(yVal);
                if (metric === "Weight") formatVal = yVal.toFixed(1);
                ctx.fillText(formatVal, padding.left - 10, yPos + 4);
            }}

            // Draw X-Axis Dates
            ctx.textAlign = "center";
            const stepX = graphWidth / (chartPeriodDays - 1);
            dates.forEach((date, i) => {{
                const xPos = padding.left + stepX * i;
                
                // Show dates depending on the selected period limits to avoid cluttering
                let show = false;
                if (chartPeriodDays === 7) show = true;
                else if (chartPeriodDays === 30 && i % 5 === 0) show = true;
                else if (chartPeriodDays === 90 && i % 15 === 0) show = true;

                if (show) {{
                    const shortDate = date.substring(5); // MM-DD
                    ctx.fillText(shortDate, xPos, height - padding.bottom + 20);
                }}
            }});

            // Draw Target Goal Line
            let goalVal = 0;
            if (metric === "Calories") goalVal = state.profile.calorieGoal;
            if (metric === "Water") goalVal = state.profile.waterGoal;
            if (metric === "Steps") goalVal = state.profile.stepsGoal;
            if (metric === "Sleep") goalVal = state.profile.sleepGoal;
            if (metric === "Protein") goalVal = Math.round((state.profile.calorieGoal * 0.3) / 4);

            if (goalVal > 0) {{
                const goalY = padding.top + graphHeight - ((goalVal - minVal) / range) * graphHeight;
                ctx.strokeStyle = "rgba(245, 158, 11, 0.35)";
                ctx.lineWidth = 1.5;
                ctx.setLineDash([5, 5]);
                ctx.beginPath();
                ctx.moveTo(padding.left, goalY);
                ctx.lineTo(width - padding.right, goalY);
                ctx.stroke();
                ctx.setLineDash([]); // Reset dash

                // Draw Goal text tag
                ctx.fillStyle = "#f59e0b";
                ctx.textAlign = "left";
                ctx.fillText("Goal", width - padding.right - 35, goalY - 6);
            }}

            // Plot actual points/bars
            const isLineChart = ["Weight", "Protein", "Sleep", "Calories"].includes(metric);
            
            // Set styles based on metric theme colors
            let lineStrokeColor = "#ff5e62";
            let fillGradientColorStart = "rgba(255, 94, 98, 0.2)";
            let fillGradientColorEnd = "rgba(255, 94, 98, 0)";

            if (metric === "Water") {{
                lineStrokeColor = "#00f2fe";
                fillGradientColorStart = "rgba(0, 242, 254, 0.25)";
            }} else if (metric === "Steps") {{
                lineStrokeColor = "#10b981";
                fillGradientColorStart = "rgba(16, 185, 129, 0.25)";
            }} else if (metric === "Sleep") {{
                lineStrokeColor = "#a78bfa";
                fillGradientColorStart = "rgba(167, 139, 250, 0.25)";
            }}

            if (isLineChart) {{
                // LINE CHART RENDERER
                ctx.beginPath();
                dates.forEach((date, i) => {{
                    const xPos = padding.left + stepX * i;
                    const yPos = padding.top + graphHeight - ((dataPoints[i] - minVal) / range) * graphHeight;
                    if (i === 0) ctx.moveTo(xPos, yPos);
                    else ctx.lineTo(xPos, yPos);
                }});
                ctx.strokeStyle = lineStrokeColor;
                ctx.lineWidth = 3.5;
                ctx.stroke();

                // Draw area gradient fill
                ctx.lineTo(padding.left + graphWidth, padding.top + graphHeight);
                ctx.lineTo(padding.left, padding.top + graphHeight);
                ctx.closePath();
                const fillGrad = ctx.createLinearGradient(0, padding.top, 0, padding.top + graphHeight);
                fillGrad.addColorStop(0, fillGradientColorStart);
                fillGrad.addColorStop(1, fillGradientColorEnd);
                ctx.fillStyle = fillGrad;
                ctx.fill();

                // Dots drawing
                dates.forEach((date, i) => {{
                    const xPos = padding.left + stepX * i;
                    const yPos = padding.top + graphHeight - ((dataPoints[i] - minVal) / range) * graphHeight;
                    ctx.beginPath();
                    ctx.arc(xPos, yPos, 4.5, 0, Math.PI * 2);
                    ctx.fillStyle = "#ffffff";
                    ctx.fill();
                    ctx.strokeStyle = lineStrokeColor;
                    ctx.lineWidth = 2.5;
                    ctx.stroke();
                }});
            }} else {{
                // BAR CHART RENDERER
                const barWidth = (graphWidth / chartPeriodDays) * 0.7;
                dates.forEach((date, i) => {{
                    const xPos = padding.left + (stepX * i) - (barWidth / 2);
                    const barHeight = ((dataPoints[i] - minVal) / range) * graphHeight;
                    const yPos = padding.top + graphHeight - barHeight;

                    // Bar fill gradient
                    const barGrad = ctx.createLinearGradient(0, yPos, 0, padding.top + graphHeight);
                    barGrad.addColorStop(0, lineStrokeColor);
                    barGrad.addColorStop(1, "rgba(255,255,255,0.01)");

                    ctx.fillStyle = barGrad;
                    
                    // Rounded top bars
                    const radius = Math.min(6, barHeight);
                    ctx.beginPath();
                    ctx.moveTo(xPos, yPos + barHeight);
                    ctx.lineTo(xPos, yPos + radius);
                    ctx.quadraticCurveTo(xPos, yPos, xPos + radius, yPos);
                    ctx.lineTo(xPos + barWidth - radius, yPos);
                    ctx.quadraticCurveTo(xPos + barWidth, yPos, xPos + barWidth, yPos + radius);
                    ctx.lineTo(xPos + barWidth, yPos + barHeight);
                    ctx.closePath();
                    ctx.fill();
                }});
            }}

            // Mouse hover tracker detection & overlay tooltip rendering
            if (mouseX >= padding.left && mouseX <= width - padding.right) {{
                // Identify index segment
                const index = Math.round((mouseX - padding.left) / stepX);
                if (index >= 0 && index < chartPeriodDays) {{
                    const hoverX = padding.left + stepX * index;
                    const hoverY = padding.top + graphHeight - ((dataPoints[index] - minVal) / range) * graphHeight;

                    // Draw vertical guides tracker
                    ctx.strokeStyle = "rgba(255, 255, 255, 0.15)";
                    ctx.lineWidth = 1;
                    ctx.setLineDash([3, 3]);
                    ctx.beginPath();
                    ctx.moveTo(hoverX, padding.top);
                    ctx.lineTo(hoverX, padding.top + graphHeight);
                    ctx.stroke();
                    ctx.setLineDash([]);

                    // Draw focus hover dot
                    ctx.beginPath();
                    ctx.arc(hoverX, hoverY, 6, 0, Math.PI * 2);
                    ctx.fillStyle = lineStrokeColor;
                    ctx.fill();
                    ctx.strokeStyle = "#fff";
                    ctx.lineWidth = 2;
                    ctx.stroke();

                    // Render tooltip container box
                    const text = `${{dataPoints[index].toLocaleString()}}`;
                    ctx.font = "bold 12px -apple-system, BlinkMacSystemFont, Segoe UI";
                    const metricsWidth = ctx.measureText(text).width;
                    
                    const tooltipW = metricsWidth + 24;
                    const tooltipH = 34;
                    let tooltipX = hoverX - (tooltipW / 2);
                    let tooltipY = hoverY - tooltipH - 8;

                    // Bound checks inside graph
                    if (tooltipX < padding.left) tooltipX = padding.left;
                    if (tooltipX + tooltipW > width - padding.right) tooltipX = width - padding.right - tooltipW;
                    if (tooltipY < padding.top) tooltipY = hoverY + 8;

                    // Background glass tooltip
                    ctx.fillStyle = "rgba(18, 20, 29, 0.95)";
                    ctx.strokeStyle = "rgba(255, 255, 255, 0.1)";
                    ctx.lineWidth = 1;
                    
                    // Rounded tooltip box drawing
                    ctx.beginPath();
                    ctx.roundRect(tooltipX, tooltipY, tooltipW, tooltipH, 8);
                    ctx.fill();
                    ctx.stroke();

                    // Text value inside tooltip
                    ctx.fillStyle = "#fff";
                    ctx.textAlign = "center";
                    ctx.fillText(text, tooltipX + (tooltipW / 2), tooltipY + 20);
                }}
            }}

            // Print summary statistics texts below graph container
            const sum = dataPoints.reduce((a, b) => a + b, 0);
            const avg = (sum / chartPeriodDays).toFixed(1);
            const min = Math.min(...dataPoints);
            const max = Math.max(...dataPoints);

            const unit = getUnitForMetric(metric);
            document.getElementById('chart-avg-val').innerText = `${{avg}} ${{unit}}`;
            document.getElementById('chart-min-val').innerText = `${{min}} ${{unit}}`;
            document.getElementById('chart-max-val').innerText = `${{max}} ${{unit}}`;
        }}

        function getUnitForMetric(metric) {{
            if (metric === "Weight") return "kg";
            if (metric === "Calories" || metric === "Burned") return "kcal";
            if (metric === "Water") return "ml";
            if (metric === "Steps") return "steps";
            if (metric === "Sleep") return "h";
            if (metric === "Protein") return "g";
            return "";
        }}

        // EVENT LISTENERS INITIALIZATION
        window.onload = function() {{
            loadState();
            initFoodDatabase();
            initGymExercises();
            renderCardioFields();
            initChartCanvasEvents();

            // Bind active date picker update handler
            document.getElementById('active-date-picker').onchange = function(e) {{
                activeDateStr = e.target.value;
                updateUI();
                if (document.getElementById('tab-analytics').classList.contains('active')) {{
                    drawAnalyticsChart();
                }}
            }};

            // Auto-save daily notes on keyup
            document.getElementById('daily-notes-input').oninput = function(e) {{
                const dayData = getActiveDayData();
                dayData.note = e.target.value;
                // Silent save
                localStorage.setItem("health-tracker", JSON.stringify(state));
            }};
        }};

        // Service Worker dynamic registration fallback logs
        if ('serviceWorker' in navigator) {{
            const swCode = `
                const CACHE_NAME = 'syncfit-cache-v1';
                const ASSETS = [
                    '/',
                    '/index.html'
                ];
                self.addEventListener('install', e => {{
                    e.waitUntil(
                        caches.open(CACHE_NAME).then(cache => {{
                            return cache.addAll(ASSETS);
                        }})
                    );
                }});
                self.addEventListener('fetch', e => {{
                    e.respondWith(
                        caches.match(e.request).then(response => {{
                            return response || fetch(e.request);
                        }})
                    );
                }});
            `;
            const blob = new Blob([swCode], {{type: 'application/javascript'}});
            const swUrl = URL.createObjectURL(blob);
            navigator.serviceWorker.register(swUrl).catch(err => {{
                console.log("Service Worker registration blocked (safe offline-first double-click default).", err);
            }});
        }}
    </script>
</body>
</html>
"""

# Write index.html to output
output_path = "index.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"Successfully compiled single-file PWA: index.html ({len(html_template)} chars)")
