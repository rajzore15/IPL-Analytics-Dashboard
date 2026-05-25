import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="IPL Analytics Dashboard",
    layout="wide",
    page_icon="🏏"
)

# ---------------- CSS ----------------
st.markdown("""
<style>

.stApp{
background: linear-gradient(135deg,#141e30,#243b55);
color:white;
}

.navbar{
display:flex;
justify-content:center;
gap:40px;
background:#0b1c3d;
padding:15px;
border-radius:10px;
margin-bottom:20px;
}

.navbar a{
color:white;
font-size:18px;
font-weight:bold;
text-decoration:none;
}

.navbar a:hover{
color:#00eaff;
}

.kpi-card{
background: rgba(255,255,255,0.1);
backdrop-filter: blur(10px);
padding:25px;
border-radius:15px;
text-align:center;
box-shadow:0 8px 30px rgba(0,0,0,0.5);
transition:0.3s;
}

.kpi-card:hover{
transform:scale(1.05);
}

.kpi-number{
font-size:40px;
font-weight:bold;
color:#00eaff;
}

.card{
background: rgba(255,255,255,0.1);
backdrop-filter: blur(10px);
padding:20px;
border-radius:15px;
box-shadow:0 8px 32px rgba(0,0,0,0.5);
text-align:center;
margin-bottom:20px;
}

.team-grid{
display:grid;
grid-template-columns: repeat(4,1fr);
gap:30px;
}

.team-card{
background: rgba(255,255,255,0.1);
backdrop-filter: blur(10px);
padding:20px;
border-radius:15px;
text-align:center;
transition:0.3s;
}

.team-card:hover{
transform:scale(1.05);
box-shadow:0 10px 40px rgba(0,0,0,0.6);
}

.team-card img{
width:120px;
height:120px;
object-fit:contain;
}

</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ----------------
st.markdown("""
<div class="navbar">
<a>MATCHES</a>
<a>TEAMS</a>
<a>STATS</a>
<a>NEWS</a>
<a>VIDEOS</a>
<a>AUCTION</a>
</div>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    matches = pd.read_csv("matches.csv")
    deliveries = pd.read_csv("deliveries.csv")
    return matches, deliveries

matches, deliveries = load_data()

# ---------------- HEADER ----------------
st.title("🏏 IPL Analytics Dashboard")

# ---------------- KPI CARDS ----------------
total_matches = matches.shape[0]

if "batsman_runs" in deliveries.columns:
    total_runs = deliveries["batsman_runs"].sum()
else:
    total_runs = 0

if "batter" in deliveries.columns:
    total_players = deliveries["batter"].nunique()
else:
    total_players = 0

if "team1" in matches.columns:
    total_teams = matches["team1"].nunique()
else:
    total_teams = 0

c1, c2, c3, c4 = st.columns(4)

c1.markdown(
    f'<div class="kpi-card"><div class="kpi-number">{total_matches}</div>Total Matches</div>',
    unsafe_allow_html=True
)

c2.markdown(
    f'<div class="kpi-card"><div class="kpi-number">{total_runs}</div>Total Runs</div>',
    unsafe_allow_html=True
)

c3.markdown(
    f'<div class="kpi-card"><div class="kpi-number">{total_players}</div>Total Players</div>',
    unsafe_allow_html=True
)

c4.markdown(
    f'<div class="kpi-card"><div class="kpi-number">{total_teams}</div>Total Teams</div>',
    unsafe_allow_html=True
)

st.divider()

# ---------------- SIDEBAR ----------------
menu = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Points Table",
        "Orange Cap",
        "Purple Cap",
        "Team Logos",
        "Match Prediction",
        "Live Scores",
        "Fixtures Timeline",
        "Data Explorer"
    ]
)

# ---------------- OVERVIEW ----------------
if menu == "Overview":

    wins = matches["winner"].value_counts()

    fig = px.bar(
        x=wins.index,
        y=wins.values,
        title="Matches Won by Teams"
    )

    st.plotly_chart(fig, use_container_width=True)

    if "batter" in deliveries.columns:

        top_runs = deliveries.groupby("batter")["batsman_runs"] \
            .sum() \
            .sort_values(ascending=False) \
            .head(10)

        fig2 = px.bar(
            x=top_runs.index,
            y=top_runs.values,
            title="Top Run Scorers"
        )

        st.plotly_chart(fig2, use_container_width=True)

# ---------------- POINTS TABLE ----------------
elif menu == "Points Table":

    wins = matches["winner"].value_counts()

    points = pd.DataFrame({
        "Team": wins.index,
        "Wins": wins.values
    })

    points["Points"] = points["Wins"] * 2

    st.dataframe(points, use_container_width=True)

# ---------------- ORANGE CAP ----------------
elif menu == "Orange Cap":

    if "batter" in deliveries.columns:

        orange = deliveries.groupby("batter")["batsman_runs"] \
            .sum() \
            .sort_values(ascending=False) \
            .head(10)

        fig = px.bar(
            x=orange.index,
            y=orange.values,
            title="Orange Cap Leaderboard"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("Batter data not available")

# ---------------- PURPLE CAP ----------------
elif menu == "Purple Cap":

    st.subheader("🟣 Purple Cap Leaderboard")

    st.info("Bowling statistics are not available in the current dataset.")

# ---------------- TEAM LOGOS ----------------
elif menu == "Team Logos":

    st.subheader("🏏 IPL Teams")

    teams = {
        "Chennai Super Kings":"https://upload.wikimedia.org/wikipedia/en/2/2e/Chennai_Super_Kings_Logo.svg",
        "Mumbai Indians":"https://upload.wikimedia.org/wikipedia/en/c/cd/Mumbai_Indians_Logo.svg",
        "Royal Challengers Bangalore":"https://upload.wikimedia.org/wikipedia/en/4/4d/Royal_Challengers_Bangalore_Logo.svg",
        "Kolkata Knight Riders":"https://upload.wikimedia.org/wikipedia/en/4/4c/Kolkata_Knight_Riders_Logo.svg",
        "Delhi Capitals":"https://upload.wikimedia.org/wikipedia/en/2/2f/Delhi_Capitals.svg",
        "Punjab Kings":"https://upload.wikimedia.org/wikipedia/en/d/d4/Punjab_Kings_Logo.svg",
        "Rajasthan Royals":"https://upload.wikimedia.org/wikipedia/en/9/9b/Rajasthan_Royals_Logo.svg",
        "Sunrisers Hyderabad":"https://upload.wikimedia.org/wikipedia/en/8/81/Sunrisers_Hyderabad.svg"
    }

    cols = st.columns(4)

    i = 0

    for team, logo in teams.items():

        with cols[i % 4]:

            st.markdown(f"""
            <div class="team-card">
                <img src="{logo}" width="120">
                <h4>{team}</h4>
            </div>
            """, unsafe_allow_html=True)

        i += 1

# ---------------- MATCH PREDICTION ----------------
elif menu == "Match Prediction":

    st.subheader("🧠 IPL Match Winner Prediction")

    df = matches[["team1", "team2", "winner"]].dropna()

    team_encoder = LabelEncoder()
    winner_encoder = LabelEncoder()

    all_teams = pd.concat([df["team1"], df["team2"]]).unique()

    team_encoder.fit(all_teams)

    df["team1"] = team_encoder.transform(df["team1"])
    df["team2"] = team_encoder.transform(df["team2"])

    df["winner"] = winner_encoder.fit_transform(df["winner"])

    X = df[["team1", "team2"]]
    y = df["winner"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestClassifier(random_state=42)

    model.fit(X_train, y_train)

    teams = sorted(matches["team1"].dropna().unique())

    t1 = st.selectbox("Team 1", teams)
    t2 = st.selectbox("Team 2", teams)

    if st.button("Predict Winner"):

        if t1 == t2:
            st.warning("Please select different teams")
        else:

            t1_enc = team_encoder.transform([t1])[0]
            t2_enc = team_encoder.transform([t2])[0]

            pred = model.predict([[t1_enc, t2_enc]])

            winner = winner_encoder.inverse_transform(pred)[0]

            st.success(f"🏆 Predicted Winner: {winner}")

# ---------------- LIVE SCORES ----------------
elif menu == "Live Scores":

    st.subheader("🔴 Live Cricket Scores")

    st.warning("Live API integration not added yet")

# ---------------- FIXTURES ----------------
elif menu == "Fixtures Timeline":

    st.subheader("📅 Upcoming Fixtures")

    for i, row in matches.head(5).iterrows():

        st.markdown(f"""
        <div class="card">
        <h3>{row['team1']} vs {row['team2']}</h3>
        <p>{row['venue']}</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------- DATA EXPLORER ----------------
elif menu == "Data Explorer":

    dataset = st.radio(
        "Dataset",
        ["Matches", "Deliveries"]
    )

    if dataset == "Matches":
        st.dataframe(matches, use_container_width=True)

    else:
        st.dataframe(deliveries, use_container_width=True)