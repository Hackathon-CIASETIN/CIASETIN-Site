# CIASETIN-Site

Site du hackathon du Club d'intelligence artificielle de l'Université Laval,
en collaboration avec l'ASETIN — 28 novembre 2026, Cafétéria Vachon.

Site statique : les pages sont servies telles quelles. Seuls les guides de rôle
passent par une étape de build.

| Chemin | Rôle |
| --- | --- |
| `index.html` | Toute la page et son contenu |
| `styles.css` | Mise en page, palette, typographie |
| `script.js` | Section courante dans le menu, neutralisation des liens vides |
| `assets/` | Logos du Club IA et de l'ASETIN, favicon |
| `guides/*.pdf` | Guides de rôle publiés — **générés, à ne pas modifier à la main** |
| `tools/build-guides.py` | Rend les guides markdown en PDF |
| `.github/workflows/deploy.yml` | Build et publication sur GitHub Pages |
| `notify-site.yml` | À déposer dans l'**autre** dépôt — voir plus bas |

## Les guides de rôle

La source de vérité est le markdown, dans l'autre dépôt :

```
CIASETIN-Documentation-Dump/Event Guides/Staffing Guides/
  juge.md
  entreprise-partenaire.md
  benevole.md
  participant.md
```

À chaque déploiement, le workflow récupère ce dossier, rend chaque fichier en PDF
dans `guides/`, et publie. Le site sert donc toujours la version la plus à jour :
**pour corriger un guide, modifiez le markdown dans le dépôt de documentation, pas
le PDF ici.** Les PDF versionnés dans `guides/` sont une commodité, pour que les
liens fonctionnent en local et à la première mise en ligne ; le build les écrase.

Pour que le site se reconstruise dès qu'un guide change, déposez `notify-site.yml`
dans `CIASETIN-Documentation-Dump/.github/workflows/`. Il faut un jeton d'accès
personnel avec `contents: write` sur ce dépôt-ci, ajouté aux secrets du dépôt de
documentation sous le nom `SITE_DISPATCH_TOKEN`. Sans ça, le site se reconstruit
quand même à chaque push ici, chaque lundi matin, et sur demande manuelle.

Si `CIASETIN-Documentation-Dump` devient privé, créez un PAT en lecture et
ajoutez-le ici comme secret `DOCS_REPO_TOKEN`.

### Reconstruire les PDF localement

```
pip install markdown playwright
playwright install chromium
python tools/build-guides.py "../CIASETIN-Documentation-Dump/Event Guides/Staffing Guides" guides
```

## Voir le site localement

Ouvrir `index.html` suffit. Pour un serveur local :

```
python -m http.server 8000
```

## Publier sur GitHub Pages

Rien à configurer à la main : `deploy.yml` active Pages lui-même au premier
passage (`configure-pages` avec `enablement: true`) et pousse le site à chaque
push sur `main`. L'adresse publique est
<https://hackathon-ciasetin.github.io/CIASETIN-Site/>.

Si quelqu'un passe dans `Settings → Pages`, la source doit rester
« GitHub Actions » — avec « Deploy from a branch », les guides ne seraient plus
régénérés.

Tant que les guides ne sont pas poussés dans le dépôt de documentation, le
workflow le signale et publie les PDF versionnés dans `guides/` tels quels : le
site se met en ligne quand même.

## À remplir avant la publication

Chaque élément est marqué `TODO Félix` dans `index.html` :

- [ ] **Lien d'inscription** — trois endroits (barre du haut, héros, section inscription)
- [ ] **Date limite d'inscription** — section `#inscription`
- [ ] **Adresse de contact du club** — section `#inscription`
- [ ] **Adresse civique exacte** de la Cafétéria Vachon, si on veut l'afficher

Les défis des partenaires ne sont pas listés sur le site : la page mentionne
seulement qu'il y a quatre catégories, dévoilées à l'ouverture.

## Notes de conception

- La palette suit la journée réelle du 28 novembre à Québec : lever 7 h 05,
  coucher 15 h 59. Le rail des heures du héros passe de l'ambre au cyan au
  coucher du soleil — la soirée du hackathon se déroule après la nuit tombée.
- Deux familles typographiques : Bricolage Grotesque pour les titres,
  Newsreader pour le texte courant. Les PDF utilisent des polices système, pour
  rester lisibles sans dépendance réseau.
- Les logos des deux clubs figurent dans la barre du haut et au pied de page,
  liés à <https://cia.ift.ulaval.ca/> et à <https://www.asetin.ca/>. Ils
  reposent sur une pastille claire : le fond encré avalerait autrement les
  traits sombres de l'écusson de l'ASETIN.
- Une seule animation, au chargement : le bloc de travail libre qui se remplit.
  Désactivée si `prefers-reduced-motion` est demandé.
