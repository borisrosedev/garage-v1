import { Router } from "@vaadin/router";
import { html, LitElement, type PropertyValues } from "lit";
import { customElement, property, state } from "lit/decorators.js";

@customElement("dashboard-view")
export class DashboardView extends LitElement {
  protected createRenderRoot(): HTMLElement | DocumentFragment {
    return this; // Utilise le DOM léger (pas de shadow DOM)
  }

  @state()
  data: any = null;

  protected async firstUpdated(_changedProperties: PropertyValues) {
    try {
      const response = await fetch("http://localhost:8000/api/v1/users/me", {
        headers: {
          "Authorization": "Bearer " + localStorage.getItem("garage:token"),
        },
      });

      if (!response.ok) {
        throw new Error("Échec de la récupération des données utilisateur");
      }

      this.data = await response.json();
    } catch (error) {
      console.error("Erreur lors de la récupération de l'utilisateur :", error);
      this.data = null;
      Router.go('/login')
    }
  }

  render() {
    if (!this.data) {
      return html`
        <main class="app__main dashboard__main">
          <h1>Dashboard</h1>
          <p>Chargement en cours ou erreur de chargement</p>
        </main>
      `;
    }

    return html`
      <main class="app__main dashboard__main">
        <h1>Dashboard</h1>
        <div class="card" style="width: 18rem;">
          ${this.data.photo_name
            ? html`<img src="http://localhost:8000/static/files/${this.data.photo_name}" class="card-img-top" alt="Photo de profil" />`
            : html`<div class="card-img-top bg-secondary text-white text-center py-4">Pas de photo</div>`}
          <div class="card-body">
            <h5 class="card-title">${this.data.firstname.charAt(0).toUpperCase() + this.data.firstname.slice(1).toLowerCase()} ${this.data.lastname.charAt(0).toUpperCase() + this.data.lastname.slice(1).toLowerCase()}</h5>
            <p class="card-text">
              Some quick example text to build on the card title and make up the bulk of the card’s content.
            </p>
          </div>
          <div class="card-body">
            <button class="btn btn-outline-success">Edit profile</button>
            <button class="btn btn-outline-danger">Delete account</button>
          </div>
        </div>
      </main>
    `;
  }
}

declare global {
  interface HTMLElementTagNameMap {
    "dashboard-view": DashboardView;
  }
}
