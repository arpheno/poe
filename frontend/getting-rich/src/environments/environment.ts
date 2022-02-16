// This file can be replaced during build by using the `fileReplacements` array.
// `ng build` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

export const environment = {
  production: false,
  whisperUrl: `http://localhost:8000/trades/whispers/`,
  itemsUrl: `http://localhost:8000/trades/`,
  horizonUrl: `http://localhost:8000/trades/ooh/`,
  gemExpUrl: `http://localhost:8000/trades/gemExp/`,
  search_resolve_url: `http://localhost:8000/trades/search/`,
  vaalurl: `http://localhost:8000/trades/gemVaal/`,
  registerUrl: `http://localhost:8000/trades/register/`,
};

/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/plugins/zone-error';  // Included with Angular CLI.
