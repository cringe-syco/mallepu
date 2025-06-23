How to explore a workflow object in R
r
Copy
Edit
library(workflows)

# Load workflow
wf <- readRDS("your_model_workflow.rds")

# Check overall structure
str(wf, max.level = 3)

# Print summary
print(wf)

# Access the recipe (preprocessing steps)
wf$pre$actions$recipe$recipe

# Access the fitted model object
wf$fit$fit

# Check the model specification (model type, engine)
wf$fit$fit$spec

# Check the model engine name
wf$fit$fit$spec$engine

# See the names of components inside workflow
names(wf)

# List preprocessing actions
names(wf$pre$actions)
What these parts mean:
wf$pre$actions$recipe$recipe: the recipe that preprocesses data (scaling, dummy variables, etc.)

wf$fit$fit: the fitted model object (e.g., a random forest or xgboost object)

wf$fit$fit$spec: the model specification object

wf$fit$fit$spec$engine: the backend engine used to fit the model

Extra: View the recipe steps
r
Copy
Edit
library(recipes)

# Print recipe steps
wf$pre$actions$recipe$recipe %>% summary()
Example: Inspect terms in recipe
r
Copy
Edit
wf$pre$actions$recipe$recipe$term_info
Summary:
Workflow combines recipe + model into one object

Explore the recipe for feature preprocessing

Explore the fitted model for parameters & type

Use print(), str(), and $ to dig in
