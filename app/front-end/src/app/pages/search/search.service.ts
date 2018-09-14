import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { Router, ActivatedRoute } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class SearchService {
  private apiUrl = 'http://localhost:8080/api/';
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
    // console.log(filters);
    for (const filter of filters) {
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
          '&pools__zones__states__code__in=' +
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
}
