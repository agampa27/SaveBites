import sys
import json
import os

print("DEBUG: Script started", file=sys.stderr, flush=True)

try:
    print("DEBUG: Parsing arguments", file=sys.stderr, flush=True)
    user_data = json.loads(sys.argv[1])
    pantry_data = json.loads(sys.argv[2])
    print(f"DEBUG: User data: {user_data}", file=sys.stderr, flush=True)
    print(f"DEBUG: Pantry data: {pantry_data}", file=sys.stderr, flush=True)
    
    API_KEY = os.environ.get('GEMINI_API_KEY')
    print(f"DEBUG: API key exists: {API_KEY is not None}", file=sys.stderr, flush=True)
    
    print("DEBUG: Importing UserProfile", file=sys.stderr, flush=True)
    from data_classes.UserProfile import UserProfile
    print("DEBUG: Importing Pantry", file=sys.stderr, flush=True)
    from data_classes.UserPantry import Pantry
    print("DEBUG: Importing RecipeLLM", file=sys.stderr, flush=True)
    from llm_pipeline.llm_recipe_generator import RecipeLLM
    print("DEBUG: Importing Ranker", file=sys.stderr, flush=True)
    from llm_pipeline.ranker import Ranker
    
    print("DEBUG: Creating user profile", file=sys.stderr, flush=True)
    user = UserProfile(
        dietary_restrictions=user_data['dietary_restrictions'],
        cuisine_preferences=user_data['cuisine_preferences'],
        budget_usd=user_data['budget_usd'],
        time_available=user_data['time_available'],
        appliances=user_data['appliances']
    )
    
    print("DEBUG: Creating pantry", file=sys.stderr, flush=True)
    pantry = Pantry(items=pantry_data['items'])
    
    print("DEBUG: Initializing RecipeLLM", file=sys.stderr, flush=True)
    recipe_llm = RecipeLLM(API_KEY)
    print("DEBUG: Initializing Ranker", file=sys.stderr, flush=True)
    ranker = Ranker(API_KEY)
    
    print("DEBUG: Generating recipes", file=sys.stderr, flush=True)
    recipes = []
    for i in range(5):
        print(f"DEBUG: Generating recipe {i+1}", file=sys.stderr, flush=True)
        recipe = recipe_llm.generate_recipes(user)
        if recipe:
            recipes.append(recipe)
            print(f"DEBUG: Recipe {i+1} generated successfully", file=sys.stderr, flush=True)
        else:
            print(f"DEBUG: Recipe {i+1} returned None", file=sys.stderr, flush=True)
    
    print(f"DEBUG: Total recipes generated: {len(recipes)}", file=sys.stderr, flush=True)
    print("DEBUG: Ranking recipes", file=sys.stderr, flush=True)
    ranked_recipes = ranker.rank(user, pantry, recipes)
    
    print("DEBUG: Creating output", file=sys.stderr, flush=True)
    output = [{
        'name': r.title,
        'ingredients': r.ingredients,
        'budget': r.price_estimate_usd,
        'time': r.cook_minutes,
        'cuisine': r.cuisine,
        'tags': r.tags
    } for r in ranked_recipes]
    
    print("DEBUG: Printing JSON output", file=sys.stderr, flush=True)
    print(json.dumps(output), flush=True)
    print("DEBUG: Script completed successfully", file=sys.stderr, flush=True)
    
except Exception as e:
    import traceback
    error_details = traceback.format_exc()
    print(f"DEBUG ERROR: {str(e)}", file=sys.stderr, flush=True)
    print(f"DEBUG TRACEBACK: {error_details}", file=sys.stderr, flush=True)
    print(json.dumps({'error': str(e), 'traceback': error_details}), file=sys.stderr, flush=True)
    sys.exit(1)