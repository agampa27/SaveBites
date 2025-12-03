import { useState } from 'react';
import './buttons.css';
import './Generate.css'

export default function Generate({pantryItems, time, difficulty, budget, allergens, appliances, cuisines }) {
	const [recipes, setRecipes] = useState([]);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState(null);

	async function generateRecipe() {
		setLoading(true);
		setError(null);
		
		try {
			const response = await fetch('http://localhost:3010/generate-recipes', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					pantryItems,
					time,
					budget,
					allergens,
					appliances,
					cuisines
				})
			});

			const data = await response.json();
			
			if (data.success) {
				setRecipes(data.recipes);
			} else {
				setError('Failed to generate recipes');
			}
		} catch (err) {
			setError('Network error: ' + err.message);
		} finally {
			setLoading(false);
		}
	}
	function recipeDisplay(recipe) {
		return (
			<p>
				Name: {recipe.name} <br />
				Ingredients: {recipe.ingredients}  <br />
				Instructions: {recipe.instructions} <br />
				Appliances: {recipe.appliances} <br />
				Budget: ${recipe.budget}
			</p>
		);
	}

	function listRecipes(recipes) {
		return (
			<ul>
				{recipes.map(item => (
					<li key={item.name}>{item.name}</li>
				))}
			</ul>
		)
	}

	return (
		<div style={{display: "flex"}}>
			<div className="box" style={{left: "10px"}}>
				<h1>Create a Recipe!</h1>

				<h3>Here are some of your ingredients: </h3>
				<div style={{position: "relative", left: "50px"}}>
						{
							// display top 7 ingredients
							pantryItems.slice(0,7).map((item) => {
								return (
									<li key={item}>{item}</li>
								)
							}
						)}
				</div>

				<h3>Your top Cuisines: </h3>
				<div style={{position: "relative", left: "50px"}}>
					{
						// display top 3 cuisines
						cuisines.slice(0,3).map((item) => {
							return (
								<li key={item}>{item}</li>
							)
						}
					)}
				</div>

				<button 
					className="btn-primary" 
					onClick={generateRecipe}
					disabled={loading}
				>
					{loading ? 'Generating...' : `Generate with $${budget} budget and ${difficulty.toLowerCase()} difficulty within ${Math.floor(time / 60)} ${Math.floor(time / 60) == 1 ? "hour" : "hours"} and ${time % 60} ${time % 60 == 1 ? "minute" : "minutes"}`}
				</button>

				{error && <p style={{color: 'red'}}>{error}</p>}

			</div>

			<div className="box" style={{left: "30px"}}>
				<h1>Generated Recipe</h1>
				{recipes.length > 0 && recipeDisplay(recipes[0])}
			</div>

			<div className="box" style={{left: "50px"}}>
				<h1> Browse more Recipes </h1>
				{recipes.length > 0 && listRecipes(recipes.slice(1,))}
			</div>

		</div>
	);
}