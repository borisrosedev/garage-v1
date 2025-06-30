import { Router } from "@vaadin/router";
import { LitElement, html, css } from "lit";
import { customElement } from "lit/decorators.js";

@customElement("login-view")
export class LoginView extends LitElement {
  protected createRenderRoot(): HTMLElement | DocumentFragment {
    return this;
  }

  private async _onSubmit(e: Event) {
    e.preventDefault();
    const submitButton = document.getElementById(
      "submit-button"
    ) as HTMLButtonElement;
    submitButton.disabled = true;

    const username = (document.querySelector("#username") as HTMLInputElement)
      .value;
    const password = (document.querySelector("#password") as HTMLInputElement)
      .value;

    if (!(username && password)) {
      alert("Fill in the form");
      submitButton.disabled = false;
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/api/v1/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          username: username,
          password: password,
        }),
      });

      const data = await response.json();
      console.log(data.access_token);
      if (!data.access_token) {
        alert("Failed to log in");
        submitButton.disabled = false;
      } else {
        localStorage.setItem("garage:token", data.access_token);
        Router.go("/dashboard");
      }
    } catch (err) {
      console.error("Erreur lors de la requête:", err);
      submitButton.disabled = false;
    }
  }

  render() {
    return html`
      <main class="app__main login__main">
        <header class="mb-5">
          <h1 style="font-size:20px">Log-in Form</h1>
        </header>
        <form id="login-form" @submit="${this._onSubmit}">
          <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input type="text" class="form-control" id="username" />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input type="password" class="form-control" id="password" />
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
    "login-view": LoginView;
  }
}
