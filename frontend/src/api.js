const API_BASE_URL = "http://localhost:8000/api";

export async function fetchLocations() {
    try {
        const res = await fetch(`${API_BASE_URL}/locations`);
        if (!res.ok) throw new Error("Failed to fetch locations");
        return await res.json();
    } catch (e) {
        console.error(e);
        return [];
    }
}

export async function fetchCuisines() {
    try {
        const res = await fetch(`${API_BASE_URL}/cuisines`);
        if (!res.ok) throw new Error("Failed to fetch cuisines");
        return await res.json();
    } catch (e) {
        console.error(e);
        return [];
    }
}

export async function fetchRecommendations(preferences) {
    const res = await fetch(`${API_BASE_URL}/recommend`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(preferences)
    });
    
    if (!res.ok) {
        throw new Error("Failed to generate recommendations");
    }
    return await res.json();
}
