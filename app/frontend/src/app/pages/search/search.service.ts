import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, tap, delay } from 'rxjs/operators';
import { Router, ActivatedRoute } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class SearchService {
  private apiUrl = window['API_HOST'] + '/api/';
  // vendors/values/pools__setasides__name
  _active_filters: any[];
  _contract_results: any[];

  search_options = {};
  constructor(
    private http: HttpClient,
    private router: Router,
    private route: ActivatedRoute
  ) {}
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
  // getAgencies(): Observable<any[]> {
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
  // getPSCs(term: string): Observable<any[]> {
  //   return this.http.get<any[]>(this.apiUrl + 'psc?description__icontains=' + term).pipe(
  //     tap(data => data),
  //     catchError(this.handleError)
  //   );
  // }
  // getContractValueHistory(): Observable<any[]> {
  //   return this.http.get<any[]>().pipe(
  //     tap(data => data),
  //     catchError(this.handleError)
  //   );
  // }
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
  arrToString(arr) {
    let str = '';
    for (const selected of arr) {
      str += arr + ',';
    }
    str = str.slice(0, -1);
    return str;
  }
  getZone(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl + 'zones/?page=0').pipe(
      tap(data => data),
      catchError(this.handleError)
    );
  }

  getKeywords(): Observable<any[]> {
    // return this.http.get<any[]>(this.apiUrl + 'keywords').pipe(delay(3000));
    return this.http.get<any[]>(this.apiUrl + 'keywords').pipe(
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

  getVendors(filters: any[]): Observable<any[]> {
    let params = '';
    for (const filter of filters) {
      if (filter['name'] === 'keywords') {
        params +=
          '&pools__pool__naics__keywords__id__in=' +
          this.getSelectedFilterList(filter['selected'], ',');
      }
      if (filter['name'] === 'vehicles') {
        params +=
          '&pools__pool__vehicle__id__in=' +
          this.getSelectedFilterList(filter['selected'], ',');
      }
      if (filter['name'] === 'service_categories') {
        params +=
          '&pools__pool__id__in=' +
          this.getSelectedFilterList(filter['selected'], ',');
      }
      if (filter['name'] === 'setasides') {
        params +=
          '&pools__setasides__code__in=' +
          this.getSelectedFilterList(filter['selected'], ',');
      }
      if (filter['name'] === 'naics') {
        params +=
          '&pools__pool__naics__code__in=' +
          this.getSelectedFilterList(filter['selected'], ',');
      }
      if (filter['name'] === 'zone') {
        params +=
          '&pools__zones__id__in=' +
          this.getSelectedFilterList(filter['selected'], ',');
      }
    }
    console.log(this.apiUrl + 'vendors?' + params.substr(1));
    return this.http
      .get<any[]>(this.apiUrl + 'vendors?' + params.substr(1))
      .pipe(
        tap(data => data),
        catchError(this.handleError)
      );
  }
  getVendorDetails(duns: string): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl + 'vendors/' + duns).pipe(
      tap(data => data),
      catchError(this.handleError)
    );
  }

  // searchDiscovery(filters: any[]): void {
  //   // let route = '';
  //   // const href = this.router.url;

  //   const params = this.getQueryParams(filters);
  //   // if (href.indexOf('vendors') > 0) {
  //   //   route = '/search/vendors';
  //   // } else {
  //   //   route = '/search/contracts';
  //   // }

  //   this.router.navigate(['search'], {
  //     queryParams: params
  //   });
  //   // this.router.navigate([route, 'results'], {
  //   //   queryParams: params
  //   // });
  //   // this.router.navigate([route, 'results'], {
  //   //   queryParams: params,
  //   //   queryParamsHandling: 'merge'
  //   // });

  //   // Get results from API
  // }
  setQueryParams(filters: any[]): void {
    // let route = '';
    // const href = this.router.url;

    const params = this.getQueryParams(filters);
    // if (href.indexOf('vendors') > 0) {
    //   route = '/search/vendors';
    // } else {
    //   route = '/search/contracts';
    // }

    this.router.navigate(['search'], {
      queryParams: params
    });
    // this.router.navigate([route, 'results'], {
    //   queryParams: params
    // });
    // this.router.navigate([route, 'results'], {
    //   queryParams: params,
    //   queryParamsHandling: 'merge'
    // });

    // Get results from API
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
      obj[filter.name] = this.getSelectedFilterList(filter.selected, '__');
    }
    return obj;
  }
  existsIn(obj: any[], value: string, key: string): boolean {
    for (let i = 0; i < obj.length; i++) {
      if (obj[i][key] === value) {
        return true;
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
    for (const i of obj) {
      items += i[key] + ', ';
    }
    return items.slice(0, -2);
  }
  sortByNameAsc(i1, i2) {
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
}
