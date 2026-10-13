import pandas as pd
import matplotlib.pyplot as plt
import folium

# --------------------------------
# Pollution Dataset
# --------------------------------
data = pd.DataFrame({

    "Area": [
        "Gachibowli","Madhapur","Hitech City","Kukatpally",
        "Ameerpet","Secunderabad","Banjara Hills",
        "Jubilee Hills","Begumpet","LB Nagar"
    ],

    "Air_Quality":[40,55,60,75,50,45,58,65,48,80],
    "Water_Quality":[60,65,55,70,62,58,64,68,59,72],
    "Noise_Level":[55,70,65,75,68,60,66,72,58,78]

})

# --------------------------------
# Pollution Index Calculation
# --------------------------------
data["Pollution_Index"] = (
    data["Air_Quality"] +
    data["Water_Quality"] +
    data["Noise_Level"]
) / 3


# --------------------------------
# Risk Prediction Function
# --------------------------------
def predict_risk(index):

    if index < 50:
        return "Low Risk"

    elif index < 70:
        return "Moderate Risk"

    else:
        return "High Risk"


data["Risk_Level"] = data["Pollution_Index"].apply(predict_risk)


# --------------------------------
# Disease Prediction Function
# --------------------------------
def predict_disease(risk):

    if risk == "Low Risk":
        return "Minimal Health Impact"

    elif risk == "Moderate Risk":
        return "Asthma / Breathing Problems"

    else:
        return "Respiratory Disease / Heart Problems"


data["Diseases"] = data["Risk_Level"].apply(predict_disease)


# --------------------------------
# Display Results
# --------------------------------
print("\nPollution Monitoring Results\n")
print(data[["Area","Pollution_Index","Risk_Level","Diseases"]])


# --------------------------------
# Pollution Graph
# --------------------------------
plt.figure()

plt.bar(data["Area"], data["Pollution_Index"])

plt.title("Pollution Index by Area")

plt.xlabel("Area")

plt.ylabel("Pollution Index")

plt.xticks(rotation=45)

plt.show()


# --------------------------------
# Create Pollution Map
# --------------------------------
map = folium.Map(location=[17.3850, 78.4867], zoom_start=11)


# Hyderabad Area Coordinates
locations = [

    [17.4401, 78.3489],   # Gachibowli
    [17.4485, 78.3908],   # Madhapur
    [17.4435, 78.3772],   # Hitech City
    [17.4948, 78.3996],   # Kukatpally
    [17.4375, 78.4482],   # Ameerpet
    [17.4399, 78.4983],   # Secunderabad
    [17.4126, 78.4482],   # Banjara Hills
    [17.4326, 78.4071],   # Jubilee Hills
    [17.4448, 78.4666],   # Begumpet
    [17.3450, 78.5480]    # LB Nagar
]


# --------------------------------
# Add Pollution Markers
# --------------------------------
for i in range(len(data)):

    risk = data["Risk_Level"][i]

    if risk == "Low Risk":
        color = "green"

    elif risk == "Moderate Risk":
        color = "orange"

    else:
        color = "red"


    popup_text = (
        "Area: " + data["Area"][i] +
        "\nPollution Index: " + str(round(data["Pollution_Index"][i],2)) +
        "\nRisk Level: " + risk +
        "\nPossible Diseases: " + data["Diseases"][i]
    )


    folium.CircleMarker(

        location = locations[i],
        radius = 10,
        popup = popup_text,
        color = color,
        fill = True,
        fill_color = color,
        fill_opacity = 0.7

    ).add_to(map)


# --------------------------------
# Add Map Legend
# --------------------------------
legend_html = '''
<div style="
position: fixed; 
bottom: 50px; left: 50px; width: 200px; height: 120px; 
background-color: white; 
border:2px solid grey; 
z-index:9999; 
font-size:14px;
padding:10px;
">
<b>Pollution Risk Levels</b><br>
🟢 Low Risk<br>
🟠 Moderate Risk<br>
🔴 High Risk
</div>
'''

map.get_root().html.add_child(folium.Element(legend_html))


# --------------------------------
# Save Map
# --------------------------------
map.save("hyderabad_pollution_map.html")

print("\nPollution Map Created Successfully!")
print("Open 'hyderabad_pollution_map.html' to view the map.")