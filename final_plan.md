Refine and finish the LM prompts calling phase one and phase two
Find goal "What does the user wish to acomplish or know?"
Then "what factors from the context fstring are relevant to this query?"
Then "quantify each of these in standard si units (note that there may be multiple of the same kind of factor e.g. time to run a mile improving over 2 months), if no SI units exist then create an appropriate ratio (e.g. academic competitiveness).
Then convert the integer (if applicable to base metric units)
this should quantify the strings, it should act as a natural language extractor (lm should be able to detect the difference between open ai and openai for instance) (it should remove the need for standard USVs as now the values are now just provided) the only place they are still useful is when there ISN'T an SI unit then we should create a var or ratio as a best guesstimate but this should be the last resort
This should remove the need for the library
Compare LM USV translator string --> lm --> int
Stripe integration
White listing
Final data flow
imput parser--> lm api --> then lines 2 through 7 --> int --> monte carlo engine --> output parser
also keep in mind we will have the goal integer and the target integer which will look like this: factor one (operator needed for monte carlo i don't know how to do this) factor two... = probability_projected (this is our guess of what will happen given relevant factors)
We will also have the target_baseline (this will also depend on the domain) which is basically the same thing which pulls from the RAG to determine what the real life probability would be then we will compare these two values probability_projected to target_baseline
Re add chain of thought with dynamic animation
Check to make sure that user authentication isn't causing issues for api keys
update .env (i will do this prompt user to do this)
pull from the factors that influence target_baseline and or the probability_projected and create a string from them informing the user what the the top 3 factors impacting their question are
See how feseable sharable odds feature would be: JPG with factors user specific odds
see whats going on with the natural language modifier right now that's causing it to default to clunky old vector system
