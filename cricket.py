import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Custom CSS for styling
def apply_custom_css():
    st.markdown("""
        <style>
            body {
                background-size: cover;
                background-repeat: no-repeat;
            }
            .main-title {
                color: white;
                font-size: 40px;
                font-family: 'Courier New', Courier, monospace;
                text-align: center;
                margin-bottom: 30px;
            }
            .sidebar .sidebar-content {
                background-color: #31333F;
                color: white;
            }
            .about-creators {
                background-color: #FAFAFA;
                padding: 20px;
                border-radius: 10px;
                color: black;
            }
            footer {
                text-align: center;
                padding: 10px;
                background-color: #2A2A2A;
                color: white;
                font-size: 12px;
                border-top: 2px solid #FFD700;
                margin-top: 20px;
            }
            .player-image {
                border-radius: 10px;
                margin-bottom: 20px;
            }
            .comparison-section {
                background-color: #FAFAFA;
                padding: 30px;
                border-radius: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

# Apply custom CSS for the design
apply_custom_css()

# Load CSV data
ball_data = pd.read_csv('each_ball_records.csv')
match_data = pd.read_csv('each_match_records.csv')
player_images = pd.read_csv('players_images.csv')  # CSV containing player names and image URLs

# Function to display player image from CSV
def display_player_image(player_name):
    image_url = player_images[player_images['player_name'] == player_name]['image_url'].values
    if len(image_url) > 0:
        st.image(image_url[0], caption=player_name, width=200, use_column_width=False)  # Standard size without unsupported class_

# Function to calculate wickets from outcome (outcome == 'w')
def calculate_wickets(player_data):
    return len(player_data[player_data['outcome'] == 'w'])

# Function to calculate economy rate (runs conceded per over)
def calculate_economy(player_data):
    total_runs_conceded = player_data['score'].sum()
    total_overs_bowled = len(player_data) / 6
    return total_runs_conceded / total_overs_bowled if total_overs_bowled > 0 else 0

# Player Statistics
def player_statistics():
    st.markdown("<h2 class='main-title'>Player Statistics</h2>", unsafe_allow_html=True)
    players = ball_data['batsman'].unique()
    selected_player = st.selectbox("Select a Player", players)

    # Filter data for the selected player
    player_batting_data = ball_data[ball_data['batsman'] == selected_player]
    player_bowling_data = ball_data[ball_data['bowler'] == selected_player]

    # Display player image
    display_player_image(selected_player)

    # Batting stats
    total_runs = player_batting_data['score'].sum()
    matches_played = player_batting_data['match_no'].nunique()
    total_balls_faced = len(player_batting_data)
    strike_rate = (total_runs / total_balls_faced) * 100 if total_balls_faced > 0 else 0

    # Bowling stats
    total_wickets = calculate_wickets(player_bowling_data)
    economy_rate = calculate_economy(player_bowling_data)

    # Display statistics
    st.write(f"Total Runs (Batting): {total_runs}")
    st.write(f"Matches Played: {matches_played}")
    st.write(f"Strike Rate (Batting): {strike_rate:.2f}")
    st.write(f"Total Wickets (Bowling): {total_wickets}")
    st.write(f"Economy Rate (Bowling): {economy_rate:.2f}")

    # Plot runs per match (Batting)
    if not player_batting_data.empty:
        runs_per_match = player_batting_data.groupby('match_no')['score'].sum()
        plt.figure(figsize=(10, 6))
        runs_per_match.plot(kind='bar', color='skyblue')
        plt.title(f"Runs Per Match for {selected_player}")
        plt.ylabel('Runs')
        plt.xlabel('Match No')
        st.pyplot(plt)
    # Plot wickets per match (Bowling)
    if not player_bowling_data.empty:
        wickets_per_match = player_bowling_data.groupby('match_no')['outcome'].apply(lambda x: (x == 'w').sum())
        plt.figure(figsize=(10, 6))
        wickets_per_match.plot(kind='bar', color='orange')
        plt.title(f"Wickets Per Match for {selected_player}")
        plt.ylabel('Wickets')
        plt.xlabel('Match No')
        st.pyplot(plt)
           
# Function to display player image from CSV
def display_player_image(player_name):
    image_url = player_images[player_images['player_name'] == player_name]['image_url'].values
    if len(image_url) > 0:
        st.image(image_url[0], caption=player_name, width=200, use_column_width=False)

# Function to plot batter comparison graph
def plot_batter_comparison(batter_1, batter_2, batter_data_1, batter_data_2):
    data = {
        'Player': [batter_1, batter_2],
        'Total Runs': [batter_data_1['score'].sum(), batter_data_2['score'].sum()],
        'Strike Rate': [
            (batter_data_1['score'].sum() / len(batter_data_1)) * 100 if len(batter_data_1) > 0 else 0,
            (batter_data_2['score'].sum() / len(batter_data_2)) * 100 if len(batter_data_2) > 0 else 0
        ]
    }
    
    df = pd.DataFrame(data)
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    sns.barplot(x='Player', y='Total Runs', data=df, ax=ax[0])
    ax[0].set_title('Total Runs Comparison')

    sns.barplot(x='Player', y='Strike Rate', data=df, ax=ax[1])
    ax[1].set_title('Strike Rate Comparison')

    st.pyplot(fig)

# Function to plot bowler comparison graph
def plot_bowler_comparison(bowler_1, bowler_2, bowler_data_1, bowler_data_2):
    data = {
        'Player': [bowler_1, bowler_2],
        'Wickets Taken': [calculate_wickets(bowler_data_1), calculate_wickets(bowler_data_2)],
        'Economy Rate': [calculate_economy(bowler_data_1), calculate_economy(bowler_data_2)]
    }

    df = pd.DataFrame(data)
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    sns.barplot(x='Player', y='Wickets Taken', data=df, ax=ax[0])
    ax[0].set_title('Wickets Taken Comparison')

    sns.barplot(x='Player', y='Economy Rate', data=df, ax=ax[1])
    ax[1].set_title('Economy Rate Comparison')

    st.pyplot(fig)

def compare_players():
    batters = ball_data['batsman'].unique()
    bowlers = ball_data['bowler'].unique()

    # Select player type for comparison
    comparison_type = st.selectbox("Select Comparison Type", ["Batter vs Bowler", "Batter vs Batter", "Bowler vs Bowler"])

    if comparison_type == "Batter vs Bowler":
        selected_batter = st.selectbox("Select Batter", batters)
        selected_bowler = st.selectbox("Select Bowler", bowlers)

        # Display images for batter and bowler
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Batter: {selected_batter}**")
            display_player_image(selected_batter)
        with col2:
            st.write(f"**Bowler: {selected_bowler}**")
            display_player_image(selected_bowler)

        # Filter data for both players
        batter_data = ball_data[ball_data['batsman'] == selected_batter]
        bowler_data = ball_data[ball_data['bowler'] == selected_bowler]

        # Batting stats for batter
        runs_scored = batter_data['score'].sum()
        balls_faced = len(batter_data)
        strike_rate_batter = (runs_scored / balls_faced) * 100 if balls_faced > 0 else 0
        matches_played_batter = batter_data['match_no'].nunique()

        # Bowling stats for bowler
        wickets_taken = calculate_wickets(bowler_data)
        economy_rate_bowler = calculate_economy(bowler_data)
        matches_played_bowler = bowler_data['match_no'].nunique()

        # Display stats for both players
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**{selected_batter} (Batter)**")
            st.write(f"Total Runs: {runs_scored}")
            st.write(f"Strike Rate: {strike_rate_batter:.2f}")
            st.write(f"Matches Played: {matches_played_batter}")

        with col2:
            st.write(f"**{selected_bowler} (Bowler)**")
            st.write(f"Total Wickets: {wickets_taken}")
            st.write(f"Economy Rate: {economy_rate_bowler:.2f}")
            st.write(f"Matches Played: {matches_played_bowler}")

        # Comparison statistics (batter vs bowler)
        comparison_data = ball_data[(ball_data['batsman'] == selected_batter) & 
                                    (ball_data['bowler'] == selected_bowler)]
        
        runs_against_bowler = comparison_data['score'].sum()
        wickets_against_batter = calculate_wickets(comparison_data)

        st.write(f"{selected_batter} scored {runs_against_bowler} runs against {selected_bowler}")
        st.write(f"{selected_bowler} took {wickets_against_batter} wickets against {selected_batter}")

    elif comparison_type == "Batter vs Batter":
        selected_batter_1 = st.selectbox("Select Batter 1", batters)
        selected_batter_2 = st.selectbox("Select Batter 2", batters)

        # Display images for both batters
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Batter 1: {selected_batter_1}**")
            display_player_image(selected_batter_1)
        with col2:
            st.write(f"**Batter 2: {selected_batter_2}**")
            display_player_image(selected_batter_2)

        # Filter data for both batters
        batter_data_1 = ball_data[ball_data['batsman'] == selected_batter_1]
        batter_data_2 = ball_data[ball_data['batsman'] == selected_batter_2]

        # Batting stats for both batters
        runs_scored_1 = batter_data_1['score'].sum()
        balls_faced_1 = len(batter_data_1)
        strike_rate_1 = (runs_scored_1 / balls_faced_1) * 100 if balls_faced_1 > 0 else 0
        matches_played_1 = batter_data_1['match_no'].nunique()

        runs_scored_2 = batter_data_2['score'].sum()
        balls_faced_2 = len(batter_data_2)
        strike_rate_2 = (runs_scored_2 / balls_faced_2) * 100 if balls_faced_2 > 0 else 0
        matches_played_2 = batter_data_2['match_no'].nunique()

        # Display stats for both batters
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**{selected_batter_1} (Batter 1)**")
            st.write(f"Total Runs: {runs_scored_1}")
            st.write(f"Strike Rate: {strike_rate_1:.2f}")
            st.write(f"Matches Played: {matches_played_1}")

        with col2:
            st.write(f"**{selected_batter_2} (Batter 2)**")
            st.write(f"Total Runs: {runs_scored_2}")
            st.write(f"Strike Rate: {strike_rate_2:.2f}")
            st.write(f"Matches Played: {matches_played_2}")

        # Add graphs for Batter vs Batter
        st.write("### Batter vs Batter Comparison Graph")
        plot_batter_comparison(selected_batter_1, selected_batter_2, batter_data_1, batter_data_2)

    elif comparison_type == "Bowler vs Bowler":
        selected_bowler_1 = st.selectbox("Select Bowler 1", bowlers)
        selected_bowler_2 = st.selectbox("Select Bowler 2", bowlers)

        # Display images for both bowlers
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Bowler 1: {selected_bowler_1}**")
            display_player_image(selected_bowler_1)
        with col2:
            st.write(f"**Bowler 2: {selected_bowler_2}**")
            display_player_image(selected_bowler_2)

        # Filter data for both bowlers
        bowler_data_1 = ball_data[ball_data['bowler'] == selected_bowler_1]
        bowler_data_2 = ball_data[ball_data['bowler'] == selected_bowler_2]

        # Bowling stats for both bowlers
        wickets_taken_1 = calculate_wickets(bowler_data_1)
        economy_rate_1 = calculate_economy(bowler_data_1)
        matches_played_1 = bowler_data_1['match_no'].nunique()

        wickets_taken_2 = calculate_wickets(bowler_data_2)
        economy_rate_2 = calculate_economy(bowler_data_2)
        matches_played_2 = bowler_data_2['match_no'].nunique()

        # Display stats for both bowlers
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**{selected_bowler_1} (Bowler 1)**")
            st.write(f"Total Wickets: {wickets_taken_1}")
            st.write(f"Economy Rate: {economy_rate_1:.2f}")
            st.write(f"Matches Played: {matches_played_1}")

        with col2:
            st.write(f"**{selected_bowler_2} (Bowler 2)**")
            st.write(f"Total Wickets: {wickets_taken_2}")
            st.write(f"Economy Rate: {economy_rate_2:.2f}")
            st.write(f"Matches Played: {matches_played_2}")

        # Add graphs for Bowler vs Bowler
        st.write("### Bowler vs Bowler Comparison Graph")
        plot_bowler_comparison(selected_bowler_1, selected_bowler_2, bowler_data_1, bowler_data_2)


def best_playing_xi():
    players = ball_data['batsman'].unique()
    selected_players = st.multiselect("Select Players for Best XI", players)

    # Calculate performance data for each player
    performance_data = []
    for player in selected_players:
        player_batting_data = ball_data[ball_data['batsman'] == player]
        player_bowling_data = ball_data[ball_data['bowler'] == player]

        total_runs = player_batting_data['score'].sum()
        total_wickets = calculate_wickets(player_bowling_data)
        economy_rate = calculate_economy(player_bowling_data)

        # Classify as batter, bowler, or all-rounder based on runs and wickets
        if total_wickets >= 2 and total_runs >= 100:  # Lower the threshold for all-rounder selection
            role = 'All-Rounder'
        elif total_wickets >= 10:
            role = 'Bowler'
        elif total_runs > 0:
            role = 'Batter'
        else:
            role = 'Unknown'  # Handle edge cases where player has little data

        performance_data.append({
            'player': player,
            'runs': total_runs,
            'wickets': total_wickets,
            'economy_rate': economy_rate,
            'role': role
        })

    # Convert to DataFrame for easier sorting
    performance_df = pd.DataFrame(performance_data)

    # Ensure there are valid roles for selection (avoiding KeyError)
    if not performance_df.empty and 'role' in performance_df.columns:
        # Select top players based on role
        best_xi = {
            'Batters': performance_df[performance_df['role'] == 'Batter'].nlargest(4, 'runs')['player'].tolist(),
            'Bowlers': performance_df[performance_df['role'] == 'Bowler'].nlargest(3, 'wickets')['player'].tolist(),
            'All-Rounders': performance_df[performance_df['role'] == 'All-Rounder'].nlargest(3, 'wickets')['player'].tolist(),
            'Wicketkeeper': [performance_df.nlargest(1, 'runs')['player'].values[0]]  # Top batter as WK
        }

        # Display Best XI
        st.write("**Best XI Team**")
        st.write("Batters: ", ", ".join(best_xi['Batters']))
        st.write("Bowlers: ", ", ".join(best_xi['Bowlers']))
        st.write("All-Rounders: ", ", ".join(best_xi['All-Rounders']))
        st.write("Wicketkeeper: ", ", ".join(best_xi['Wicketkeeper']))

# Function: Winning Predictor
def winning_predictor():
    teams = match_data['team1'].unique()
    selected_team1 = st.selectbox("Select Team 1", teams)
    selected_team2 = st.selectbox("Select Team 2", teams)

    toss_winner = st.selectbox("Toss Winner", [selected_team1, selected_team2])
    toss_decision = st.selectbox("Toss Decision", ["Bat", "Field"])

    venue = st.selectbox("Select Venue", match_data['venue'].unique())

    # Filter data based on the selected venue and teams
    filtered_matches = match_data[
        ((match_data['team1'] == selected_team1) & (match_data['team2'] == selected_team2)) |
        ((match_data['team1'] == selected_team2) & (match_data['team2'] == selected_team1))
    ]

    # Further filter based on the venue
    venue_filtered_matches = filtered_matches[filtered_matches['venue'] == venue]

    # Basic prediction logic based on toss and venue history
    if toss_decision == "Bat":
        predicted_winner = toss_winner  # Assuming the team that bats first has an advantage
    else:
        # Use historical data to find which team wins more at the selected venue
        if len(venue_filtered_matches) > 0:
            venue_winner_counts = venue_filtered_matches['winner'].value_counts()
            predicted_winner = venue_winner_counts.idxmax() if not venue_winner_counts.empty else "No Prediction"
        else:
            predicted_winner = "No Prediction"

    # Display prediction
    st.write(f"**Predicted Winner**: {predicted_winner}")

# Home Page
def home_page():
    st.image("ipl_2023.jpg", use_column_width=True)
    st.markdown("<h1 class='main-title'>Welcome to Cricket Stats Predictor!</h1>", unsafe_allow_html=True)
    st.write("""
        This platform allows you to explore and analyze cricket statistics, 
        compare players, generate the best playing XI, and predict match outcomes based on past data.
        Use the navigation sidebar to explore different sections of the app.
    """)

# About the Creators
def about_creators():
    st.markdown("<h2 class='main-title'>About the Creators</h2>", unsafe_allow_html=True)
    st.write("We are a team of passionate cricket enthusiasts and data scientists who believe in harnessing the power of data to bring insights into the game we all love.")
    st.markdown("""
        <div class="about-creators">
            <p>Creators:</p>
            <ul>
                <li><b>Karnatakam Hitesh</b></li>
                <li>Gadiraju Shanthan</li>
                <li>Kaushal Sandri</li>
                <li>Ramisetti Vagdevi</li>
                <li>Theppa Pranathi</li>
            </ul>
            <p>Get in touch with us at <strong>contact@cricketstats.com</strong>.</p>
        </div>
    """, unsafe_allow_html=True)

# Navigation Sidebar
st.sidebar.title("Navigation")
pages = ["Home", "Player Statistics", "Compare Players", "Best Playing XI", "Winning Team Predictor", "About Creators"]
selected_page = st.sidebar.selectbox("Select a Feature", pages)

# Routing
if selected_page == "Home":
    home_page()
elif selected_page == "Player Statistics":
    player_statistics()
elif selected_page == "Compare Players":
    compare_players()
elif selected_page == "Best Playing XI":
    best_playing_xi()
elif selected_page == "Winning Team Predictor":
    winning_predictor()
elif selected_page == "About Creators":
    about_creators()

# Footer
st.markdown("<footer>© 2024 Cricket Stats Predictor</footer>", unsafe_allow_html=True)
