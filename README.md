## Frontend 

### Lit 

Creating a Lit component involves a number of concepts:

- Defining a component:

A Lit component is implemented as a custom element, registered with the browser.

- Rendering. 

A component has render method that's called to render the component's contents. In the render method, you define a template for the component.


Reactive properties. Properties hold the state of the component. Changing one or more of the components' reactive properties triggers an update cycle, re-rendering the component.

Styles. A component can define encapsulated styles to control its own appearance.

Lifecycle. Lit defines a set of callbacks that you can override to hook into the component's lifecycle—for example, to run code when the element's added to a page, or whenever the component updates.


## Backend

### OAuth2PasswordBearer

Il s'agit d’une dépendance de sécurité fourni par FastAPI pour extraire et valider un token d'accès (Authorization: Bearer <token>) depuis les requêtes entrantes.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

#### tokenUrl="/api/v1/auth/login"



Ce paramètre doit correspondre à l'URL du endpoint où les utilisateurs vont s'authentifier pour obtenir un token.