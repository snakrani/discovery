import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, tap, delay } from 'rxjs/operators';
import { Router, ActivatedRoute } from '@angular/router';
import { PARAMETERS } from '@angular/core/src/util/decorators';
declare let API_HOST: string;
declare const $: any;
@Injectable({
  providedIn: 'root'
})
export class SearchService {
  private apiUrl = API_HOST + '/api/';
  _pools;
  _keywords;
  _active_filters: any[];
  _contract_results: any[];
  _total_vendors_per_vehicle: any[];
  _countries: any[];
  _states: any[];

  search_options = {};

  constructor(
    private http: HttpClient,
    private router: Router,
    private route: ActivatedRoute
  ) {}
  get pools(): any[] {
    return this._pools;
  }
  set pools(arr: any[]) {
    this._pools = arr;
  }
  get keywords(): any[] {
    return this._keywords;
  }
  set keywords(arr: any[]) {
    this._keywords = arr;
  }
  get total_vendors_per_vehicle(): any[] {
    return this._total_vendors_per_vehicle;
  }
  set total_vendors_per_vehicle(arr: any[]) {
    this._total_vendors_per_vehicle = arr;
  }
  get activeFilters(): any[] {
    return this._active_filters;
  }
  set activeFilters(arr: any[]) {
    this._active_filters = arr;
  }
  get contractResults(): any[] {
    return this._contract_results;
  }
  set contractResults(arr: any[]) {
    this._contract_results = arr;
  }
  get countries(): any[] {
    return this._countries;
  }
  set countries(arr: any[]) {
    this._countries = arr;
  }
  get states(): any[] {
    return this._states;
  }
  set states(arr: any[]) {
    this._states = arr;
  }
  setSearchOptions(key: string, values: any[]): void {
    this.search_options[key] = values;
  }
  getSearchOptions(key: string): string[] {
    return this.search_options[key];
  }
  getContractVehicles(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl + 'vehicles').pipe(
      tap(data => data),
      catchError(this.handleError)
    );
  }
  // getCertifications(): Observable<any[]> {
  //   return this.http.get<any[]>(this.apiUrl).pipe(
  //     tap(data => data),
  //     catchError(this.handleError)
  //   );
  // }
  getPSCsByTerm(str: string): Observable<any[]> {
    return this.http
      .get<any[]>(this.apiUrl + 'psc?description__contains=' + str)
      .pipe(
        tap(data => data),
        catchError(this.handleError)
      );
  }
  getPSCsByNAICs(naics): Observable<any[]> {
    return this.http
      .get<any[]>(
        this.apiUrl + 'psc?naics__code__in=' + this.arrToString(naics)
      )
      .pipe(
        tap(data => data),
        catchError(this.handleError)
      );
  }
  getContractPricingType(): Observable<any[]> {
    return this.http
      .get<any[]>(this.apiUrl + 'contracts/values/pricing_type__name')
      .pipe(
        tap(data => data),
        catchError(this.handleError)
      );
  }
  getSetAsides(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl + 'setasides?description').pipe(
      tap(data => data),
      catchError(this.handleError)
    );
  }
  getServiceCategories(vehicles): Observable<any[]> {
    if (vehicles[0] === 'All') {
      return this.http.get<any[]>(this.apiUrl + 'pools?page=0').pipe(
        tap(data => data),
        catchError(this.handleError)
      );
    } else {
      return this.http
        .get<any[]>(
          this.apiUrl + 'pools?vehicle__id__in=' + this.arrToString(vehicles)
        )
        .pipe(
          tap(data => data),
          catchError(this.handleError)
        );
    }
  }
  getPools(vehicles): Observable<any[]> {
    if (vehicles[0] === 'All') {
      return this.http.get<any[]>(this.apiUrl + 'pools?page=0').pipe(
        tap(data => data),
        catchError(this.handleError)
      );
    } else {
      return this.http
        .get<any[]>(
          this.apiUrl + 'pools?vehicle__id__in=' + this.arrToString(vehicles)
        )
        .pipe(
          tap(data => data),
          catchError(this.handleError)
        );
    }
  }

  getZone(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl + 'zones/?page=0').pipe(
      tap(data => data),
      catchError(this.handleError)
    );
  }

  getKeywords(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl + 'keywords?page=0').pipe(
      tap(data => data),
      catchError(this.handleError)
    );
  }
  getPoolsByVehicle(vehicle: string): Observable<any[]> {
    return this.http
      .get<any[]>(this.apiUrl + 'pools?vehicle__id=' + vehicle)
      .pipe(
        tap(data => data),
        catchError(this.handleError)
      );
  }
  getNaics(vehicles): Observable<any[]> {
    if (vehicles[0] === 'All') {
      return this.http.get<any[]>(this.apiUrl + 'pools').pipe(
        tap(data => data),
        catchError(this.handleError)
      );
    } else {
      return this.http
        .get<any[]>(
          this.apiUrl + 'pools?vehicle__id__in=' + this.arrToString(vehicles)
        )
        .pipe(
          tap(data => data),
          catchError(this.handleError)
        );
    }
  }
  getNaicsCodes(vehicle): Observable<any[]> {
    return this.http
      .get<any[]>(
        this.apiUrl + 'pools/values/naics__code?vehicle__id=' + vehicle
      )
      .pipe(
        tap(data => data),
        catchError(this.handleError)
      );
  }
  getPlaceOfPerformance(): Observable<any[]> {
    return this.http
      .get<any[]>(this.apiUrl + 'placesofperformance/?page=0')
      .pipe(
        tap(data => data),
        catchError(this.handleError)
      );
  }

  getVendors(filters: any[], page: string, vehicle: string): Observable<any[]> {
    let params = '';
    if (vehicle) {
      params += '%28pool__vehicle__id=' + vehicle + '%29';
    }
    params += this.buildOtherParams(filters);
    if (page) {
      params += page;
    }
    console.log(this.apiUrl + 'vendors?membership=' + params);
    return this.http
      .get<any[]>(this.apiUrl + 'vendors?membership=' + params)
      .pipe(
        tap(data => data),
        catchError(this.handleError)
      );
  }
  buildOtherParams(filters): string {
    let params = '';
    for (const filter of filters) {
      if (filter['name'] === 'keywords') {
        for (const keyword of filter['selected']) {
          params += '%26%28pool__keywords__id=' + keyword['value'] + '%29';
        }
      }
      if (filter['name'] === 'service_categories') {
        for (const cat of filter['selected']) {
          params += '%26%28pool__id=' + cat['value'] + '%29';
        }
      }
      if (filter['name'] === 'setasides') {
        for (const setaside of filter['selected']) {
          params += '%26%28setasides__code=' + setaside['value'] + '%29';
        }
      }
      if (filter['name'] === 'naics') {
        for (const naic of filter['selected']) {
          params += '%26%28pool__naics__code=' + naic['value'] + '%29';
        }
      }
      if (filter['name'] === 'pscs') {
        for (const psc of filter['selected']) {
          params += '%26%28pool__psc__code=' + psc['value'] + '%29';
        }
      }
      if (filter['name'] === 'zone') {
        for (const zone of filter['selected']) {
          params += '%26%28zones__id=' + zone['value'] + '%29';
        }
      }
      if (filter['name'] === 'pop') {
        params +=
          '%26%28contract__place_of_performance__country_code=' +
          filter['selected'][0].value +
          '%29';
        if (filter['selected'][1]) {
          params +=
            '%26%28contract__place_of_performance__state=' +
            filter['selected'][1].value +
            '%29';
        }
      }
      if (filter['name'] === 'obligated_amount') {
        const threshold = filter['selected'][0].value;
        params +=
          '%26%28contract__obligated_amount__range=0,' + threshold + '%29';
      }
      if (filter['name'] === 'agency_performance') {
        for (const agency of filter['selected']) {
          params += '%26%28contract__agency__id=' + agency['value'] + '%29';
        }
      }
    }
    return params;
  }
  getVehicleVendorsMeetCriteria(
    filters: any[],
    vehicle: string
  ): Observable<any[]> {
    let params = '';
    params += '%28pool__vehicle__id=' + vehicle + '%29';
    params += this.buildOtherParams(filters);
    console.log(this.apiUrl + 'vendors/count/duns?membership=' + params);
    return this.http
      .get<any[]>(this.apiUrl + 'vendors/count/duns?membership=' + params)
      .pipe(
        tap(data => data),
        catchError(this.handleError)
      );
  }
  generateUniqueID(): string {
    return (
      '_' +
      Math.random()
        .toString(36)
        .substr(2, 9)
    );
  }
  getVehiclesToCompare(filters: any[]): Observable<any[]> {
    let params = '';
    for (const filter of filters) {
      if (filter['name'] === 'vehicles') {
        params +=
          '&vehicle__id__in=' +
          this.getSelectedFilterList(filter['selected'], ',');
      }
      if (filter['name'] === 'keywords') {
        params +=
          '&keywords__id__in=' +
          this.getSelectedFilterList(filter['selected'], ',');
      }
      if (filter['name'] === 'naics') {
        params +=
          '&naics__code__in=' +
          this.getSelectedFilterList(filter['selected'], ',');
      }
      if (filter['name'] === 'pscs') {
        params +=
          '&psc__code__in=' +
          this.getSelectedFilterList(filter['selected'], ',');
      }
    }
    console.log(this.apiUrl + 'pools/values/vehicle?' + params.substr(1));
    return this.http
      .get<any[]>(this.apiUrl + 'pools/values/vehicle?' + params.substr(1))
      .pipe(
        tap(data => data),
        catchError(this.handleError)
      );
  }

  getVendorsCountByVehicle(vehicle: string): Observable<any[]> {
    return this.http
      .get<any[]>(
        this.apiUrl + 'vendors/count/id?pools__pool__vehicle__id=' + vehicle
      )
      .pipe(
        tap(data => data),
        catchError(this.handleError)
      );
  }
  getObligatedAmountDuns(range: string): Observable<any[]> {
    const arr = range.split('-');
    const from = arr[0];
    const to = arr[1];
    return this.http
      .get<any[]>(
        this.apiUrl +
          'contracts/values/vendor__duns?obligated_amount__range=' +
          from +
          ',' +
          to
      )
      .pipe(
        tap(data => data),
        catchError(this.handleError)
      );
  }
  getAgencyPerformanceNames(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl + 'agencies/?page=0').pipe(
      tap(data => data),
      catchError(this.handleError)
    );
  }
  getAgencyPerformanceDuns(ids: string): Observable<any[]> {
    return this.http
      .get<any[]>(
        this.apiUrl + 'contracts/values/vendor__duns?agency_id__in=' + ids
      )
      .pipe(
        tap(data => data),
        catchError(this.handleError)
      );
  }
  getVendorDetails(duns: string): Observable<any[]> {
    console.log(this.apiUrl + 'vendors/' + duns);
    return this.http.get<any[]>(this.apiUrl + 'vendors/' + duns).pipe(
      tap(data => data),
      catchError(this.handleError)
    );
  }
  getVendorContractHistory(
    duns: string,
    page: string,
    piid: string,
    naic: string,
    country: string,
    state: string,
    ordering: string
  ): Observable<any[]> {
    let params = 'contracts?vendor__duns=' + duns;
    if (naic !== 'All') {
      params += '&psc_naics=' + naic;
    }
    if (piid !== 'All') {
      params += '&base_piid__in=' + piid;
    }
    if (country !== '0') {
      params += '&place_of_performance__country_code=' + country;
    }
    if (state !== '0') {
      params += '&place_of_performance__state=' + state;
    }
    if (ordering !== '') {
      params += '&ordering=' + ordering;
    }
    console.log(this.apiUrl + params + page);
    return this.http.get<any[]>(this.apiUrl + params + page).pipe(
      tap(data => data),
      catchError(this.handleError)
    );
  }
  arrToString(arr) {
    let str = '';
    for (const selected of arr) {
      str += selected + ',';
    }
    str = str.slice(0, -1);
    return str;
  }
  setQueryParams(filters: any[]): void {
    const params = this.getQueryParams(filters);
    this.router.navigate(['search'], {
      queryParams: params
    });
  }
  private handleError(err: HttpErrorResponse) {
    let errorMessage = '';
    if (err.error instanceof ErrorEvent) {
      errorMessage = 'An error occurred: ' + err.error.message;
    } else {
      errorMessage =
        'Server returned code: ' +
        err.status +
        ', error message is: ' +
        err.message;
    }
    console.error(errorMessage);
    return throwError(errorMessage);
  }

  getSelectedFilterList(arr: any[], concat: string): string {
    let str = '';
    for (const selected of arr) {
      str += selected['value'] + concat;
    }
    str = str.slice(0, -concat.length);
    return str;
  }
  getQueryParams(arr: any[]): any[] {
    const obj = [];
    for (const filter of arr) {
      obj[filter.name] = this.getSelectedFilterList(filter['selected'], '__');
    }
    return obj;
  }
  existsIn(obj: any[], value: string, key: string): boolean {
    for (let i = 0; i < obj.length; i++) {
      if (key !== '') {
        if (obj[i][key] === value) {
          return true;
        }
      } else {
        if (obj[i] === value) {
          return true;
        }
      }
    }
    return false;
  }
  getItemDescription(
    obj: any[],
    value: string,
    key_id: string,
    key_desc: string
  ): string {
    if (value) {
      for (let i = 0; i < obj.length; i++) {
        if (obj[i][key_id] === value) {
          return obj[i][key_desc];
        }
      }
    }
  }
  commaSeparatedList(obj: any[], key: string) {
    let items = '';
    if (key !== '') {
      for (const i of obj) {
        items += i[key] + ', ';
      }
    } else {
      for (const i of obj) {
        items += i + ', ';
      }
    }
    return items.slice(0, -2);
  }
  getPageNumber(str): number {
    const params = str.split('&');
    let n = 0;
    for (const item of params) {
      if (item.indexOf('page=') !== -1) {
        const arr = item.split('=');
        n = arr[1];
      }
    }
    return n;
  }
  buildKeywordsDropdown(obj: any[]): any[] {
    const keywords = [];
    for (const item of obj) {
      const keyword = {};
      keyword['text'] = item['name'];
      keyword['id'] = item['id'];
      keywords.push(keyword);
    }
    return keywords;
  }

  sortByNameAsc(i1, i2) {
    if (i1.name > i2.name) {
      return 1;
    } else if (i1.name === i2.name) {
      return 0;
    } else {
      return -1;
    }
  }
  sortByValueAsc(i1, i2) {
    if (i1 > i2) {
      return 1;
    } else if (i1 === i2) {
      return 0;
    } else {
      return -1;
    }
  }
  sortByIdAsc(i1, i2) {
    if (i1.id > i2.id) {
      return 1;
    } else if (i1.id === i2.id) {
      return 0;
    } else {
      return -1;
    }
  }
  sortByCodeAsc(i1, i2) {
    if (i1.code > i2.code) {
      return 1;
    } else if (i1.code === i2.code) {
      return 0;
    } else {
      return -1;
    }
  }
  sortByTextAsc(i1, i2) {
    if (i1.text > i2.text) {
      return 1;
    } else if (i1.text === i2.text) {
      return 0;
    } else {
      return -1;
    }
  }
  sortByDescriptionAsc(i1, i2) {
    if (i1.description > i2.description) {
      return 1;
    } else if (i1.description === i2.description) {
      return 0;
    } else {
      return -1;
    }
  }
  sortByVehicleAsc(i1, i2) {
    if (i1.vehicle > i2.vehicle) {
      return 1;
    } else if (i1.vehicle === i2.vehicle) {
      return 0;
    } else {
      return -1;
    }
  }
  sortByNumberAsc(i1, i2) {	
    var number1 = parseInt(i1.number, 10);	
    var number2 = parseInt(i2.number, 10);	
    if (number1 > number2) {	
      return 1;	
    } else if (number1 === number2) {	
      return 0;	
    } else {	
      return -1;	
    }	
  }
}
