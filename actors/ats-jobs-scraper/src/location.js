// Greenhouse hardcodes no city/country/region: it publishes one free-text string
// (`location.name`) that boards fill in by hand, so the same board mixes
// "United States", "San Francisco, CA", "Bengaluru, India" and "Remote - Texas".
// This module turns that string into structured fields, and ONLY when the text
// actually names a place we recognise. A wrong country is worse than a null one.
//
// MEASURED DECISION (cycle 607, 1,912 live postings on airbnb/databricks/figma/
// stripe/discord): `offices[].name` is NOT used as a fallback. It looks tempting
// (stripe pairs the bare city "Dublin" with the office "Ireland Locations") but
// databricks' offices routinely contradict the posting: a "Finland" posting
// carries a "Denmark" office, "Nevada" carries "Remote - Texas", "New Jersey"
// carries "San Francisco, California". Inferring country from it would invent
// wrong answers on one board to fill nulls on another.

const COUNTRIES = new Map();
function country(canonical, ...aliases) {
  for (const a of [canonical, ...aliases]) COUNTRIES.set(a.toLowerCase(), canonical);
}
country('United States', 'USA', 'US', 'U.S.', 'U.S.A.', 'United States of America', 'America');
country('United Kingdom', 'UK', 'U.K.', 'Great Britain', 'Britain');
country('Canada'); country('Ireland'); country('Germany', 'Deutschland');
country('France'); country('Spain'); country('Italy'); country('Portugal');
country('Netherlands', 'The Netherlands', 'Holland'); country('Belgium');
country('Luxembourg'); country('Switzerland'); country('Austria');
country('Sweden'); country('Norway'); country('Denmark'); country('Finland');
country('Iceland'); country('Poland'); country('Czech Republic', 'Czechia');
country('Slovakia'); country('Hungary'); country('Romania'); country('Bulgaria');
country('Greece'); country('Serbia'); country('Croatia'); country('Slovenia');
country('Estonia'); country('Latvia'); country('Lithuania'); country('Ukraine');
country('Turkey', 'Türkiye'); country('Israel'); country('United Arab Emirates', 'UAE');
country('Saudi Arabia'); country('Qatar'); country('Egypt'); country('Morocco');
country('South Africa'); country('Nigeria'); country('Kenya'); country('Ghana');
country('India'); country('Pakistan'); country('Bangladesh'); country('Sri Lanka');
country('China'); country('Hong Kong'); country('Taiwan'); country('Japan');
country('South Korea', 'Korea', 'Republic of Korea'); country('Singapore');
country('Malaysia'); country('Indonesia'); country('Thailand'); country('Vietnam');
country('Philippines', 'The Philippines'); country('Australia'); country('New Zealand');
country('Mexico'); country('Brazil', 'Brasil'); country('Argentina'); country('Chile');
country('Colombia'); country('Peru'); country('Uruguay'); country('Costa Rica');
country('Panama'); country('Guatemala'); country('Dominican Republic');

// Sub-national regions. Value is [canonicalRegion, country].
const REGIONS = new Map();
function region(canonical, countryName, ...aliases) {
  for (const a of [canonical, ...aliases]) REGIONS.set(a.toLowerCase(), [canonical, countryName]);
}
const US_STATES = [
  ['Alabama', 'AL'], ['Alaska', 'AK'], ['Arizona', 'AZ'], ['Arkansas', 'AR'],
  ['California', 'CA'], ['Colorado', 'CO'], ['Connecticut', 'CT'], ['Delaware', 'DE'],
  ['Florida', 'FL'], ['Hawaii', 'HI'], ['Idaho', 'ID'], ['Illinois', 'IL'],
  ['Indiana', 'IN'], ['Iowa', 'IA'], ['Kansas', 'KS'], ['Kentucky', 'KY'],
  ['Louisiana', 'LA'], ['Maine', 'ME'], ['Maryland', 'MD'], ['Massachusetts', 'MA'],
  ['Michigan', 'MI'], ['Minnesota', 'MN'], ['Mississippi', 'MS'], ['Missouri', 'MO'],
  ['Montana', 'MT'], ['Nebraska', 'NE'], ['Nevada', 'NV'], ['New Hampshire', 'NH'],
  ['New Jersey', 'NJ'], ['New Mexico', 'NM'], ['New York', 'NY'], ['North Carolina', 'NC'],
  ['North Dakota', 'ND'], ['Ohio', 'OH'], ['Oklahoma', 'OK'], ['Oregon', 'OR'],
  ['Pennsylvania', 'PA'], ['Rhode Island', 'RI'], ['South Carolina', 'SC'],
  ['South Dakota', 'SD'], ['Tennessee', 'TN'], ['Texas', 'TX'], ['Utah', 'UT'],
  ['Vermont', 'VT'], ['Virginia', 'VA'], ['Washington', 'WA'], ['West Virginia', 'WV'],
  ['Wisconsin', 'WI'], ['Wyoming', 'WY'], ['Puerto Rico', 'PR'],
];
// NOTE: "Georgia" is deliberately absent — as a bare token it is equally the US
// state and the country, and we will not guess. Same for the 2-letter code "GA".
for (const [name, abbr] of US_STATES) region(name, 'United States', abbr);
region('District of Columbia', 'United States', 'DC', 'D.C.', 'Washington D.C.', 'Washington DC', 'Washington, D.C.');
for (const [name, abbr] of [
  ['Alberta', 'AB'], ['British Columbia', 'BC'], ['Manitoba', 'MB'], ['New Brunswick', 'NB'],
  ['Newfoundland and Labrador', 'NL'], ['Nova Scotia', 'NS'], ['Ontario', 'ON'],
  ['Prince Edward Island', 'PE'], ['Quebec', 'QC', 'Québec'], ['Saskatchewan', 'SK'],
]) region(name, 'Canada', abbr);
region('England', 'United Kingdom');
region('Scotland', 'United Kingdom');
region('Wales', 'United Kingdom');
region('Northern Ireland', 'United Kingdom');

// City gazetteer, used only when the string names a city with no country/region
// beside it ("Dublin", "Bengaluru"). Entries whose bare name is genuinely
// ambiguous across countries are omitted on purpose: Cambridge, Birmingham,
// Victoria, Springfield, Hyderabad(-Pakistan), Santiago, Valencia, San Jose.
const CITIES = new Map();
function city(canonical, regionName, countryName, ...aliases) {
  for (const a of [canonical, ...aliases]) CITIES.set(a.toLowerCase(), [canonical, regionName, countryName]);
}
city('San Francisco', 'California', 'United States');
city('South San Francisco', 'California', 'United States');
city('Mountain View', 'California', 'United States');
city('Palo Alto', 'California', 'United States');
city('Sunnyvale', 'California', 'United States');
city('San Mateo', 'California', 'United States');
city('Los Angeles', 'California', 'United States');
city('San Diego', 'California', 'United States');
city('Seattle', 'Washington', 'United States');
city('Bellevue', 'Washington', 'United States');
city('New York', 'New York', 'United States', 'New York City', 'NYC');
city('Brooklyn', 'New York', 'United States');
city('Boston', 'Massachusetts', 'United States');
city('Chicago', 'Illinois', 'United States');
city('Austin', 'Texas', 'United States');
city('Dallas', 'Texas', 'United States');
city('Houston', 'Texas', 'United States');
city('Denver', 'Colorado', 'United States');
city('Atlanta', 'Georgia', 'United States');
city('Miami', 'Florida', 'United States');
city('Philadelphia', 'Pennsylvania', 'United States');
city('Minneapolis', 'Minnesota', 'United States');
city('Salt Lake City', 'Utah', 'United States');
city('Pittsburgh', 'Pennsylvania', 'United States');
city('Nashville', 'Tennessee', 'United States');
city('Raleigh', 'North Carolina', 'United States');
city('Detroit', 'Michigan', 'United States');
city('Toronto', 'Ontario', 'Canada');
city('Ottawa', 'Ontario', 'Canada');
city('Waterloo', 'Ontario', 'Canada');
city('Montreal', 'Quebec', 'Canada', 'Montréal');
city('Vancouver', 'British Columbia', 'Canada');
city('Calgary', 'Alberta', 'Canada');
city('London', 'England', 'United Kingdom');
city('Manchester', 'England', 'United Kingdom');
city('Edinburgh', 'Scotland', 'United Kingdom');
city('Glasgow', 'Scotland', 'United Kingdom');
city('Belfast', 'Northern Ireland', 'United Kingdom');
city('Dublin', null, 'Ireland');
city('Cork', null, 'Ireland');
city('Paris', null, 'France');
city('Lyon', null, 'France');
city('Berlin', null, 'Germany');
city('Munich', null, 'Germany', 'München');
city('Hamburg', null, 'Germany');
city('Frankfurt', null, 'Germany');
city('Cologne', null, 'Germany', 'Köln');
city('Amsterdam', null, 'Netherlands');
city('Rotterdam', null, 'Netherlands');
city('Brussels', null, 'Belgium', 'Bruxelles');
city('Zurich', null, 'Switzerland', 'Zürich');
city('Geneva', null, 'Switzerland');
city('Vienna', null, 'Austria', 'Wien');
city('Madrid', null, 'Spain');
city('Barcelona', null, 'Spain');
city('Lisbon', null, 'Portugal', 'Lisboa');
city('Porto', null, 'Portugal');
city('Milan', null, 'Italy', 'Milano');
city('Rome', null, 'Italy', 'Roma');
city('Stockholm', null, 'Sweden');
city('Gothenburg', null, 'Sweden');
city('Copenhagen', null, 'Denmark', 'København');
city('Oslo', null, 'Norway');
city('Helsinki', null, 'Finland');
city('Warsaw', null, 'Poland', 'Warszawa');
city('Krakow', null, 'Poland', 'Kraków', 'Cracow');
city('Wroclaw', null, 'Poland', 'Wrocław');
city('Prague', null, 'Czech Republic', 'Praha');
city('Budapest', null, 'Hungary');
city('Bucharest', null, 'Romania');
city('Sofia', null, 'Bulgaria');
city('Belgrade', null, 'Serbia', 'Beograd');
city('Athens', null, 'Greece');
city('Tallinn', null, 'Estonia');
city('Vilnius', null, 'Lithuania');
city('Riga', null, 'Latvia');
city('Istanbul', null, 'Turkey');
city('Tel Aviv', null, 'Israel', 'Tel Aviv-Yafo');
city('Dubai', null, 'United Arab Emirates');
city('Abu Dhabi', null, 'United Arab Emirates');
city('Cairo', null, 'Egypt');
city('Nairobi', null, 'Kenya');
city('Lagos', null, 'Nigeria');
city('Cape Town', null, 'South Africa');
city('Johannesburg', null, 'South Africa');
city('Bengaluru', null, 'India', 'Bangalore');
city('Mumbai', null, 'India');
city('New Delhi', null, 'India');
city('Gurgaon', null, 'India', 'Gurugram');
city('Noida', null, 'India');
city('Pune', null, 'India');
city('Chennai', null, 'India');
city('Tokyo', null, 'Japan');
city('Osaka', null, 'Japan');
city('Seoul', null, 'South Korea');
city('Beijing', null, 'China');
city('Shanghai', null, 'China');
city('Shenzhen', null, 'China');
city('Taipei', null, 'Taiwan');
city('Bangkok', null, 'Thailand');
city('Jakarta', null, 'Indonesia');
city('Kuala Lumpur', null, 'Malaysia');
city('Manila', null, 'Philippines');
city('Ho Chi Minh City', null, 'Vietnam');
city('Hanoi', null, 'Vietnam');
city('Sydney', 'New South Wales', 'Australia');
city('Melbourne', 'Victoria', 'Australia');
city('Brisbane', 'Queensland', 'Australia');
city('Perth', 'Western Australia', 'Australia');
city('Auckland', null, 'New Zealand');
city('Wellington', null, 'New Zealand');
city('Mexico City', null, 'Mexico', 'Ciudad de México', 'CDMX');
city('Guadalajara', null, 'Mexico');
city('Monterrey', null, 'Mexico');
city('Sao Paulo', null, 'Brazil', 'São Paulo');
city('Rio de Janeiro', null, 'Brazil');
city('Buenos Aires', null, 'Argentina');
city('Bogota', null, 'Colombia', 'Bogotá');
city('Lima', null, 'Peru');

// Multi-city areas that are not a single city but do pin a region/country.
const AREAS = new Map([
  ['san francisco bay area', [null, 'California', 'United States']],
  ['bay area', [null, 'California', 'United States']],
  ['greater seattle area', [null, 'Washington', 'United States']],
  ['new york metro area', [null, 'New York', 'United States']],
  ['greater boston area', [null, 'Massachusetts', 'United States']],
]);

// Tokens that look like a place but name none: multi-country zones, US compass
// quadrants (Databricks writes "Central - United States"), catch-alls and board
// placeholders. Matched on the whole normalised token.
const NON_PLACES = new Set([
  'remote', 'n/a', 'na', 'none', 'tbd', 'unknown', 'various', 'multiple', 'multiple locations',
  'anywhere', 'worldwide', 'global', 'flexible', 'hybrid', 'onsite', 'on-site', 'field',
  'emea', 'apac', 'amer', 'americas', 'latam', 'nam', 'usca', 'eu', 'europe', 'asia',
  'asia pacific', 'north america', 'south america', 'africa', 'middle east', 'oceania',
  'international', 'other', 'virtual', 'distributed', 'location', 'headquarters', 'hq',
  'north', 'south', 'east', 'west', 'central', 'midwest', 'mountain', 'pacific',
  'northeast', 'northwest', 'southeast', 'southwest', 'west coast', 'east coast',
]);
// Substrings that mark a token as an area/zone rather than a single city.
const AREA_RE = /\b(area|region|metro|corridor|zone|territory|nationwide|countrywide)\b/i;

function norm(s) {
  return String(s ?? '').replace(/\s+/g, ' ').trim();
}
// Lookup key: lowercase, and periods dropped so "Washington D.C." and
// "Washington DC" are the same token.
function key(s) {
  return norm(s).toLowerCase().replace(/\./g, '').trim();
}
// Re-key the vocabularies through key() so registration and lookup agree.
for (const m of [COUNTRIES, REGIONS, CITIES, AREAS]) {
  for (const [k, v] of [...m.entries()]) {
    const kk = key(k);
    if (kk !== k) m.set(kk, v);
  }
}

// Removes the remote/hybrid decoration a board wraps around a real place:
// "Remote USA", "(Remote) London", "Remote in the US". Dashed forms
// ("Remote - California", "US-Remote") are handled by the tokenizer instead,
// which drops "Remote" as a NON_PLACE token.
function stripRemote(s) {
  let out = norm(s).replace(/\((?:remote|hybrid|on-?site)\)/gi, ' ');
  // Only a bare leading "Remote" is dropped here. "Remote - California" keeps its
  // dash so the tokenizer can split it; eating the dash would leave "- California".
  out = norm(out).replace(/^remote\s+(?:in\s+(?:the\s+)?)?(?=[A-Za-z0-9(])/i, '');
  // A trailing "Remote" after a SPACED dash must take the dash with it. Dropping the
  // word alone left a dangling separator ("Florida - Remote" -> "Florida -"), and the
  // tokenizer only splits a dash with space on BOTH sides, so the string then matched
  // nothing — Workday's "<place> - Remote" convention (salesforce, adobe) lost the place
  // entirely. Verified cycle 609: "Florida - Remote", "California - Remote", "Japan -
  // Remote" all parsed to three nulls before this.
  // Two guards, both measured over 1,910 live Greenhouse postings rather than assumed —
  // each one was added only after a wider version of this rule shipped wrong data in test:
  //   * the space before the dash is REQUIRED. An UNspaced "CC-Remote" is the country-
  //     prefix convention the tokenizer splits on its own, and eating that dash corrupted
  //     multi-city lists: "Chicago, US-Remote, Canada-Remote" became "Chicago, US-Remote,
  //     Canada" and resolved to city "US-Remote" in Canada. 7 distinct strings regressed.
  //   * a comma list is left alone. In "NYC, SF, Seattle, US - Remote" the trailing "US"
  //     is the country of the WHOLE list, so removing the dash promoted the last-listed
  //     city (Seattle) over the primary one (NYC), against the leftmost-wins rule above.
  //     Keeping the dangling dash there preserves the pre-existing fallback that gets it
  //     right. Only the simple "<place> - Remote" form — which is what Workday's
  //     salesforce/adobe boards actually write — is rewritten.
  if (!out.includes(',')) out = norm(out).replace(/\s+[-–—]\s+remote$/i, '');
  out = norm(out).replace(/\s+remote$/i, '');
  return norm(out);
}

function lookupRegion(token) {
  return REGIONS.get(key(token)) ?? null;
}
function lookupCountry(token) {
  const k = key(token);
  // A bare 2-letter token inside a location string is a state/province code by
  // board convention ("San Francisco, CA"), never an ISO country code — the only
  // short country aliases we honour are the ones boards actually write out.
  if (/^[a-z]{2}$/.test(k) && !['us', 'uk'].includes(k)) return null;
  return COUNTRIES.get(k) ?? null;
}

// Splits a location string into place tokens. Commas are the main separator;
// a spaced dash ("Remote - California", "Northeast - United States") and
// Stripe's "CC-City" prefix ("US-San Francisco", "CA-Toronto", "NYC-Privy")
// are the two board conventions that also separate places.
function tokenize(s) {
  return s
    .split(',')
    .flatMap((t) => t.split(/\s+[-–—]\s+/))
    .flatMap((t) => t.split(/(?<=^[A-Za-z]{2,3})-(?=[A-Za-z])/))
    .map(norm)
    .filter(Boolean);
}

// Normalises a token before it is accepted as a city, and returns null when the
// token cannot be one. Boards append site labels ("South San Francisco HQ") and
// Stripe writes internal airport-style codes ("SF", "SEA", "CHI", "ATL") that we
// will not expand by guessing — only gazetteer aliases such as NYC survive.
function cityToken(tok) {
  const t = norm(tok).replace(/\s+(hq|headquarters|office|campus|site)$/i, '');
  if (!t || NON_PLACES.has(key(t)) || AREA_RE.test(t)) return null;
  if (CITIES.has(key(t))) return t;
  if (t.length <= 4 && t === t.toUpperCase() && /[A-Z]/.test(t)) return null;
  return t;
}

/**
 * Parse a Greenhouse free-text location into { city, region, country }.
 * Any field we are not confident about stays null.
 */
export function parseLocation(raw) {
  const empty = { city: null, region: null, country: null };
  let s = norm(raw);
  if (!s) return empty;

  // A posting may list several places ("Mountain View, California; San Francisco,
  // California", "SF • NYC", "Dublin or London"). The first one is the primary;
  // the rest are already exposed through `secondaryLocations`.
  s = norm(s.split(/\s*[•;|]\s*|\s+\/\s+|\s+or\s+/i)[0]);
  s = stripRemote(s);
  if (!s) return empty;

  const whole = AREAS.get(key(s));
  if (whole) return { city: whole[0], region: whole[1], country: whole[2] };
  if (NON_PLACES.has(key(s))) return empty;

  const tokens = tokenize(s);
  if (!tokens.length) return empty;

  // Scan left to right for the first token that is a region or a country. Going
  // left-to-right (not right-to-left) keeps the PRIMARY place when a board packs
  // a whole list into one comma string: "San Francisco, CA, Chicago, IL, New
  // York, NY" must resolve to San Francisco, not New York.
  let city = null;
  let region = null;
  let country = null;
  let matchedAt = -1;
  for (let i = 0; i < tokens.length; i += 1) {
    let r = lookupRegion(tokens[i]);
    // "Washington, DC" and "New York, NY" put a region-shaped name in the CITY
    // slot. When two region tokens sit side by side the first one is the city.
    if (r && i + 1 < tokens.length && lookupRegion(tokens[i + 1])) r = null;
    const c = r ? null : lookupCountry(tokens[i]);
    if (!r && !c) continue;
    if (r) { [region, country] = r; } else { country = c; }
    matchedAt = i;
    // The token immediately before is the city, unless it is itself a place name
    // ("San Francisco, California, United States" -> city stays San Francisco).
    // A gazetteer city always wins that test, because plenty of real cities share
    // their region's name ("New York, New York").
    if (i > 0) {
      const prev = cityToken(tokens[i - 1]);
      if (prev && (CITIES.has(key(prev)) || (!lookupRegion(prev) && !lookupCountry(prev)))) city = prev;
    }
    // A country may follow the region: "London, England, United Kingdom".
    if (r && i + 1 < tokens.length) {
      const next = lookupCountry(tokens[i + 1]);
      if (next) country = next;
    }
    break;
  }

  if (matchedAt < 0) {
    // No country or region anywhere: the string may still lead with a bare city
    // ("Dublin", "Atlanta, Georgia", "NYC, SF"). Only the FIRST token is tried,
    // and only against the curated gazetteer.
    const g = CITIES.get(key(cityToken(tokens[0]) ?? ''));
    if (!g) return empty;
    return { city: g[0], region: g[1], country: g[2] };
  }

  // Country-first convention ("US-San Francisco", "US-Remote, Chicago"): the city
  // follows the country. Only accepted for a gazetteer city in that same country,
  // so a stray token can never become a city.
  if (!city && matchedAt === 0 && country) {
    for (let i = 1; i < tokens.length; i += 1) {
      const g = CITIES.get(key(tokens[i]));
      if (g && g[2] === country) { city = g[0]; region = region ?? g[1]; break; }
      // "US-NY": the country prefix may be followed by its own region code.
      const r2 = lookupRegion(tokens[i]);
      if (!region && r2 && r2[1] === country) { region = r2[0]; }
    }
  }

  if (city) {
    const g = CITIES.get(key(city));
    if (g) {
      if (g[2] === country) {
        // The gazetteer is curated and the board text is hand-typed, so once the
        // country agrees the gazetteer's region is the better answer. "New York
        // City, Washington DC, Remote" is a list of two cities, not a city in DC.
        city = g[0];
        region = g[1];
      } else {
        // Country conflict: "Toronto, NY, SEA, SF" would otherwise file Toronto
        // under New York. Keep the city, drop geography we know is contradicted.
        city = g[0];
        region = null;
        country = null;
      }
    } else if (matchedAt > 1) {
      // The region/country matched two or more tokens in, so it belongs to some
      // later entry of a list rather than to this city ("SF, SEA, NY, Remote-US").
      region = null;
    }
  } else if (matchedAt > 1) {
    region = null;
  }
  return { city: city || null, region: region || null, country: country || null };
}
