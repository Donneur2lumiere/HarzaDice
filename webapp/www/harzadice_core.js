// Logique métier de HarzaDice — port JS fidèle de harzadice_core.py
// Hasard "cryptographique suffisant mais pas réel" : crypto.getRandomValues
// (PRNG du navigateur/système), entropie renforcée sans TRNG matériel.

// Symboles : ★ critique, ☠ fumble (universellement rendus)
const DE_FIN = '\u2605';
const DE_FUMBLE = '\u2620';

// Probabilités par couleur (identiques à harzadice_core.py)
const DES_PROBAS = {
  R: { values: [DE_FIN, DE_FUMBLE, 0, 1, 2], weights: [1, 3, 8, 2, 2] },
  O: { values: [DE_FIN, DE_FUMBLE, 0, 1, 2], weights: [1, 1, 7, 5, 2] },
  N: { values: [DE_FIN, DE_FUMBLE, 0, 1, 2], weights: [1, 1, 6, 5, 3] },
  V: { values: [DE_FIN, DE_FUMBLE, 0, 1, 2], weights: [1, 1, 5, 5, 4] },
  B: { values: [DE_FIN, DE_FUMBLE, 0, 1, 2], weights: [3, 1, 3, 4, 5] },
};

// Effets (cas critiques) — identiques à harzadice_core.py
const CAS2 = 'Désarmé, -1 Ԭ si dragonne, Si 2* dragonne casse ou -2 Ԭ';
const CAS3 = 'Arme brisée';
const CAS4 = 'Chute -1🎲, & -1 Ԭ pour se relever, -1🎲 -1 Ԭ sup pour 2M';
const CAS5 = 'Se blesse ɸ4, C 1M 1*Đ, 2M D 2*Đ';
const CAS6 = 'Perte de doigt, -1🎲 Permanent';
const CAS7 = 'S’assomme = fin du combat pour vous';

const EFFETS = {
  C: { 2: CAS2, 3: CAS3, 4: CAS4, 5: CAS5, 6: CAS6, 7: CAS7 },
  M: { 2: CAS2, 3: CAS3, 4: CAS4, 5: CAS5, 6: CAS6, 7: CAS7 },
  D: { 2: CAS2, 3: CAS3, 4: CAS4, 5: CAS5 },
};

const TYPES_ARME = ['C', 'M', 'D'];
const TYPE_ARME_LIBELLE = { C: 'Courte', M: 'Moyenne', D: 'Distante' };

const COULEURS = [
  { code: 'R', libelle: 'Rouge', hex: '#c0392b' },
  { code: 'O', libelle: 'Orange', hex: '#e67e22' },
  { code: 'N', libelle: 'Noir', hex: '#2c2c2c' },
  { code: 'V', libelle: 'Vert', hex: '#27ae60' },
  { code: 'B', libelle: 'Bleu', hex: '#2980b9' },
];

// --- Hasard cryptographique (crypto.getRandomValues) ---
function _randInt(max) {
  // Entier uniforme dans [0, max) via crypto.getRandomValues.
  const maxUint32 = 0xFFFFFFFF;
  if (max <= 0) return 0;
  const limit = maxUint32 - (maxUint32 % max);
  const arr = new Uint32Array(1);
  let r;
  do {
    crypto.getRandomValues(arr);
    r = arr[0];
  } while (r >= limit);
  return r % max;
}

function lancerDe(couleur, nombre = 1) {
  const spec = DES_PROBAS[couleur];
  const total = spec.weights.reduce((a, b) => a + b, 0);
  const resultats = [];
  for (let i = 0; i < nombre; i++) {
    const tirage = _randInt(total);
    let cumul = 0;
    for (let j = 0; j < spec.weights.length; j++) {
      cumul += spec.weights[j];
      if (tirage < cumul) {
        resultats.push(spec.values[j]);
        break;
      }
    }
  }
  return resultats;
}

function calculerResultat(resultats, typeArme) {
  let nbEtoiles = 0, nbFumbles = 0;
  for (const r of resultats) {
    if (r === DE_FIN) nbEtoiles++;
    else if (r === DE_FUMBLE) nbFumbles++;
  }

  let valeurSymboles, nbRestants, symbolesRestants, effet, partie;
  if (nbEtoiles > nbFumbles) {
    valeurSymboles = 4;
    nbRestants = nbEtoiles - nbFumbles;
    symbolesRestants = Array(nbRestants).fill(DE_FIN);
    if (nbRestants === 1) {
      effet = 'Vous avez gagné 4 touches !';
      partie = 'Attaquant';
    } else {
      effet = EFFETS[typeArme][nbRestants] || '';
      partie = 'Défenseur';
    }
  } else if (nbFumbles > nbEtoiles) {
    valeurSymboles = -2;
    nbRestants = nbFumbles - nbEtoiles;
    symbolesRestants = Array(nbRestants).fill(DE_FUMBLE);
    if (nbRestants === 1) {
      effet = 'Vous avez perdu 2 touches et votre adversaire en a gagné 1';
      partie = 'Attaquant';
    } else {
      effet = EFFETS[typeArme][nbRestants] || '';
      partie = 'Attaquant';
    }
  } else {
    valeurSymboles = 0;
    symbolesRestants = [];
    effet = '';
    partie = '';
  }

  let sommeNumerique = 0;
  for (const r of resultats) {
    if (typeof r === 'number') sommeNumerique += r;
  }
  return {
    total: sommeNumerique + valeurSymboles,
    symbolesRestants,
    effet,
    partie,
    resultats,
  };
}

function lancerSelection(selection, typeArme) {
  const resultats = [];
  for (const c of COULEURS) {
    const n = selection[c.code] || 0;
    if (n > 0) resultats.push(...lancerDe(c.code, n));
  }
  return calculerResultat(resultats, typeArme);
}

// Export pour tests (Node) si disponible
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    DE_FIN, DE_FUMBLE, DES_PROBAS, EFFETS, TYPES_ARME,
    TYPE_ARME_LIBELLE, COULEURS, lancerDe, calculerResultat, lancerSelection,
  };
}
