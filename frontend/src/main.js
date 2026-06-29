import { fetchLocations, fetchCuisines, fetchRecommendations } from './api.js';

document.addEventListener('DOMContentLoaded', async () => {
    // 1. DOM Elements
    const locationSelect = document.getElementById('location-select');
    const cuisineSelect = document.getElementById('cuisine-select');
    const form = document.getElementById('preferences-form');
    const submitBtn = document.getElementById('submit-btn');
    const errorBar = document.getElementById('error-bar');
    const errorMessage = document.getElementById('error-message');
    
    const welcomeState = document.getElementById('welcome-state');
    const loadingState = document.getElementById('loading-state');
    const cardsList = document.getElementById('cards-list');
    const noResults = document.getElementById('no-results');
    const summaryBanner = document.getElementById('summary-banner');
    const summaryText = document.getElementById('summary-text');

    // 2. Initialize dropdowns
    try {
        const [locations, cuisines] = await Promise.all([fetchLocations(), fetchCuisines()]);
        
        // Populate locations
        locationSelect.innerHTML = ''; // Clear loading option
        if (locations.length === 0) {
            locationSelect.innerHTML = '<option value="" disabled>Backend API offline</option>';
            showError("Backend is unreachable. Please make sure the FastAPI server is running.");
        } else {
            locations.forEach(loc => {
                const opt = document.createElement('option');
                opt.value = loc;
                opt.textContent = loc;
                locationSelect.appendChild(opt);
            });
            // Pre-select Bellandur if it exists
            const hasBellandur = locations.find(l => l.toLowerCase() === 'bellandur');
            if (hasBellandur) locationSelect.value = hasBellandur;
        }

        // Populate cuisines
        cuisines.forEach(c => {
            const opt = document.createElement('option');
            opt.value = c;
            opt.textContent = c;
            cuisineSelect.appendChild(opt);
        });
    } catch (err) {
        showError("Failed to fetch initial data. Is the backend running?");
    }

    // 3. Handle Form Submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Hide previous errors/states
        errorBar.classList.add('hidden');
        welcomeState.classList.add('hidden');
        cardsList.classList.add('hidden');
        noResults.classList.add('hidden');
        summaryBanner.classList.add('hidden');
        
        // Show loading
        loadingState.classList.remove('hidden');
        submitBtn.disabled = true;
        submitBtn.classList.add('opacity-75', 'cursor-not-allowed');

        const prefs = {
            location: locationSelect.value,
            budget: document.getElementById('budget-select').value,
            min_rating: parseFloat(document.getElementById('rating-slider').value)
        };
        
        const cuisineVal = cuisineSelect.value;
        if (cuisineVal) {
            prefs.cuisine = cuisineVal;
        }
        
        const additional = document.getElementById('additional-context').value.trim();
        if (additional) {
            prefs.additional_preferences = additional;
        }

        try {
            const response = await fetchRecommendations(prefs);
            loadingState.classList.add('hidden');
            
            if (response.recommendations && response.recommendations.length > 0) {
                renderCards(response.recommendations);
                cardsList.classList.remove('hidden');
                
                if (response.summary) {
                    summaryText.textContent = `"${response.summary}"`;
                    summaryBanner.classList.remove('hidden');
                }
            } else {
                noResults.classList.remove('hidden');
            }
        } catch (err) {
            loadingState.classList.add('hidden');
            showError("Failed to get recommendations. Please try again.");
            welcomeState.classList.remove('hidden'); // Fallback to welcome
        } finally {
            submitBtn.disabled = false;
            submitBtn.classList.remove('opacity-75', 'cursor-not-allowed');
        }
    });

    function renderCards(recommendations) {
        cardsList.innerHTML = '';
        
        // Gold for #1, Silver for #2, Bronze for #3
        const rankColors = {
            1: '#D4AF37',
            2: '#C0C0C0',
            3: '#CD7F32'
        };

        recommendations.forEach(rec => {
            const rankColor = rankColors[rec.rank] || '#5c5c5c';
            
            const card = document.createElement('article');
            card.className = "bg-surface-container-lowest rounded-xl overflow-hidden card-shadow border border-outline-variant/20 transition-all duration-300 group";
            
            // Generate cuisine chips
            const cuisineChips = rec.cuisine.split(',').map(c => 
                `<span class="px-2 py-1 bg-surface-container-high rounded text-[11px] font-medium text-on-surface-variant">${c.trim()}</span>`
            ).join('');

            card.innerHTML = `
                <div class="relative h-2 bg-primary">
                    <!-- Rank Badge overlaying the top slightly -->
                    <div class="absolute top-2 left-4 bg-surface-container-lowest rounded-lg shadow-sm px-3 py-1 flex items-center gap-1 border border-outline-variant/50 z-10">
                        <span class="font-headline-sm text-headline-sm font-bold" style="color: ${rankColor}">#${rec.rank}</span>
                        <span class="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">Match</span>
                    </div>
                </div>
                <div class="p-5 pt-10">
                    <div class="flex justify-between items-start mb-2">
                        <div>
                            <h4 class="font-headline-sm text-headline-sm text-on-surface font-bold group-hover:text-primary transition-colors">${rec.restaurant_name}</h4>
                            <div class="flex flex-wrap gap-2 mt-2">
                                ${cuisineChips}
                            </div>
                        </div>
                        <div class="flex flex-col items-end">
                            <div class="flex items-center gap-1 bg-green-600 text-white px-2 py-1 rounded-md shadow-sm">
                                <span class="font-label-md text-label-md font-bold">${rec.rating}</span>
                                <span class="material-symbols-outlined fill text-[14px]">star</span>
                            </div>
                            <span class="font-label-sm text-label-sm text-on-surface-variant mt-1">₹${rec.cost_for_two} for two</span>
                        </div>
                    </div>
                    <div class="mt-4 pt-4 border-t border-outline-variant/30">
                        <p class="font-body-md text-body-md text-on-surface-variant">
                            <span class="font-semibold text-on-surface">Why it matches:</span> ${rec.explanation}
                        </p>
                    </div>
                    <div class="mt-4 flex items-center justify-between text-sm text-on-surface-variant">
                        <span>Match Score</span>
                        <span class="font-bold text-primary">${rec.match_score}/10</span>
                    </div>
                </div>
            `;
            cardsList.appendChild(card);
        });
    }

    function showError(msg) {
        errorMessage.textContent = msg;
        errorBar.classList.remove('hidden');
        setTimeout(() => {
            errorBar.classList.add('hidden');
        }, 5000);
    }
});
