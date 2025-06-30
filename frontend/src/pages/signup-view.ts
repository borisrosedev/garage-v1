import { LitElement, html, css } from "lit";
import { customElement } from "lit/decorators.js";

@customElement("signup-view")
export class SignupView extends LitElement {
  protected createRenderRoot(): HTMLElement | DocumentFragment {
    return this;
  }

  private hasNullFieldValue(data: FormData): boolean {
    for (const [key, value] of data.entries()) {
      if (value === null || value === "") {
        return true;
      }
    }
    return false;
  }

  private async _onSubmit(e: MouseEvent) {
    e.preventDefault();

    const submitButton = document.getElementById(
      "submit-button"
    ) as HTMLButtonElement;
    submitButton.disabled = true;



    const formData = new FormData(
      document.getElementById("signup-form") as HTMLFormElement
    );


    if(this.hasNullFieldValue(formData)) {
 
      alert('Fill in the form');
      submitButton.disabled = false;
      return;
  

    }


    const requestInit = {
      method: "POST",
      body: formData
    }

    try {
      const serverReponse = await fetch(
        "http://localhost:3000/api/v1/users/create",requestInit 
      );
      const jsResponse = await serverReponse.json();
      console.log(jsResponse);
    } catch (err) {
      console.log(err);
      submitButton.disabled = false;
    }
  }

  render() {
    return html`
      <main class="app__main signup__main">
        <header class="mb-5">
          <h1 style="font-size:20px">Sign-up Form</h1>
        </header>

        <form
          id="signup-form"
          @submit="${this._onSubmit}"
          enctype="multipart/form-data"
        >
          <div class="mb-3">
            <label for="firstname" class="form-label">Firstname</label>
            <input
              type="text"
              class="form-control"
              name="firstname"
              id="firstname"
            />
          </div>
          <div class="mb-3">
            <label for="lastname" class="form-label">Lastname</label>
            <input
              type="text"
              class="form-control"
              name="lastname"
              id="lastname"
            />
          </div>
          <div class="mb-3">
            <label for="email" class="form-label">Email address</label>
            <input type="email" class="form-control" name="email" id="email" />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input
              type="password"
              class="form-control"
              name="password"
              id="password"
            />
          </div>
          <div class="mb-3">
            <label for="photo" class="form-label">Photo</label>
            <input class="form-control" type="file" name="photo" id="photo" />
          </div>
          <button id="submit-button" type="submit" class="btn btn-primary">
            Submit
          </button>
        </form>
      </main>
    `;
  }
}

declare global {
  interface HTMLElementTagNameMap {
    "signup-view": SignupView;
  }
}
