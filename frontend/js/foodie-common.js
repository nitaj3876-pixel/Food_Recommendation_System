/* Foodie - shared frontend helpers */

// ---------- Backend URL ----------
// Local dev default. When you deploy, change ONLY this one line to your
// deployed backend's URL (e.g. "https://foodie-api.onrender.com") -
// every page reads it from here instead of hardcoding its own copy.
const API_BASE = "http://127.0.0.1:8000";

// ---------- Emoji fallback (shown only if no local photo file is found) ----------
const FOOD_EMOJI_MAP = [
  ["pizza", "🍕"], ["burger", "🍔"], ["biryani", "🍛"], ["curry", "🍛"],
  ["spaghetti", "🍝"], ["pasta", "🍝"], ["sushi", "🍣"], ["dosa", "🥞"],
  ["paneer", "🧀"], ["tikka", "🍢"], ["chicken", "🍗"], ["ice cream", "🍨"],
  ["smoothie", "🥤"], ["avocado", "🥑"], ["toast", "🍞"], ["sandwich", "🥪"],
  ["wrap", "🌯"], ["chickpea", "🫘"], ["quinoa", "🥣"], ["buckwheat", "🥣"],
  ["bowl", "🥣"], ["vegetable", "🥦"], ["veggie", "🥦"], ["salad", "🥗"],
  ["fruit", "🍓"],
];

function foodEmoji(food) {
  const haystack = `${food.name || ""} ${food.category || ""} ${food.tags || ""}`.toLowerCase();
  for (const [keyword, emoji] of FOOD_EMOJI_MAP) {
    if (haystack.includes(keyword)) return emoji;
  }
  return "🍽️";
}

// Turns a food name into the filename we expect in frontend/images/
// e.g. "Grilled Chicken Salad" -> "grilled-chicken-salad"
function foodSlug(food) {
  return (food.name || "food")
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
}

// Called from the <img onerror="..."> below.
// stage 1: the .jpg failed -> try .png next.
// stage 2: the .png also failed -> give up and show the emoji instead.
function handleFoodImgError(img, slug, stage) {
  if (stage === 1) {
    img.src = `images/${slug}.png`;
    img.setAttribute("onerror", `handleFoodImgError(this, '${slug}', 2)`);
  } else {
    img.style.display = "none";
    if (img.nextElementSibling) img.nextElementSibling.style.display = "flex";
  }
}

// Renders a food thumbnail that looks for a local photo first
// (frontend/images/<slug>.jpg, then .png) and falls back to an emoji tile
// if neither file exists. food.image_url (if set by an admin) always wins.
function foodThumbHtml(food, extraClass = "") {
  const slug = foodSlug(food);
  const src = food.image_url || `images/${slug}.jpg`;
  const emoji = foodEmoji(food);
  return `<div class="thumb-icon ${extraClass}" style="position:relative; padding:0;" aria-hidden="true">
      <img src="${src}" alt="" style="width:100%;height:100%;object-fit:cover;border-radius:inherit;display:block;"
           onerror="handleFoodImgError(this, '${slug}', 1)">
      <span style="display:none; position:absolute; inset:0; align-items:center; justify-content:center; font-size:54px;">${emoji}</span>
    </div>`;
}

// ---------- Click-through: open the "related to this food" view ----------
function relatedUrl(food) {
  return `recommend.html?food=${food.id}`;
}
