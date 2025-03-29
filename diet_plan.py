def generate_diet_plan(condition, weight, allergies, preferences):
    """Generate a personalized diet plan based on user inputs"""
    plans = {
        'diabetes': f"Low-carb diet ({weight*20}kcal/day). Focus on high-fiber foods and lean proteins.",
        'hypertension': f"Low-sodium diet ({weight*25}kcal/day). Rich in potassium-rich foods.",
        'weight-loss': f"Calorie deficit diet ({weight*22}kcal/day). High protein, moderate carbs.",
        'weight-gain': f"Calorie surplus diet ({weight*35}kcal/day). Focus on protein and complex carbs.",
        'general': f"Balanced diet ({weight*30}kcal/day). Variety of whole foods."
    }
    
    base_plan = plans.get(condition, plans['general'])
    
    # Add preferences
    if preferences == 'vegetarian':
        base_plan += "\nVegetarian options: Plant-based proteins like beans and tofu."
    elif preferences == 'vegan':
        base_plan += "\nVegan options: No animal products, focus on plant proteins."
    elif preferences == 'gluten-free':
        base_plan += "\nGluten-free options: Avoid wheat, barley, rye."
    
    # Add allergy warnings
    if allergies:
        base_plan += f"\nAllergy Alert: Avoid {allergies}."
    
    return base_plan

def generate_sample_meals(condition, preferences, allergies):
    """Generate sample meals based on condition and preferences"""
    meals = {
        'breakfast': '',
        'lunch': '',
        'dinner': '',
        'snacks': ''
    }
    
    # Base meals for different conditions
    if condition == 'diabetes':
        meals.update({
            'breakfast': 'Greek yogurt with berries and nuts',
            'lunch': 'Grilled chicken salad with olive oil',
            'dinner': 'Baked salmon with quinoa and veggies',
            'snacks': 'Celery sticks with almond butter'
        })
    elif condition == 'hypertension':
        meals.update({
            'breakfast': 'Oatmeal with banana and flaxseeds',
            'lunch': 'Lentil soup with whole grain bread',
            'dinner': 'Grilled turkey with sweet potatoes',
            'snacks': 'Unsalted nuts and fresh fruit'
        })
    else:  # General health
        meals.update({
            'breakfast': 'Scrambled eggs with whole grain toast',
            'lunch': 'Quinoa bowl with mixed vegetables',
            'dinner': 'Grilled fish with brown rice',
            'snacks': 'Yogurt with granola'
        })
    
    # Adjust for preferences
    if preferences == 'vegetarian':
        meals['lunch'] = 'Chickpea salad with tahini'
        meals['dinner'] = 'Vegetable stir-fry with tofu'
    elif preferences == 'vegan':
        meals['breakfast'] = 'Smoothie with almond milk and chia seeds'
        meals['dinner'] = 'Vegan chili with beans'
    elif preferences == 'gluten-free':
        meals['breakfast'] = meals['breakfast'].replace('toast', 'gluten-free toast')
        meals['lunch'] = meals['lunch'].replace('bread', 'gluten-free bread')
    
    return "\n".join([f"{meal.capitalize()}: {details}" for meal, details in meals.items()])

def generate_shopping_list(meals):
    """Generate shopping list from sample meals"""
    ingredients = set()
    common_items = ['water', 'salt', 'pepper', 'oil']
    
    for line in meals.split('\n'):
        if ':' in line:
            items = line.split(':')[1].strip().lower()
            for item in items.split(','):
                item = item.strip()
                if item and item not in common_items:
                    ingredients.add(item)
    
    return sorted(ingredients)