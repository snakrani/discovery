import { Injectable } from '@angular/core';
import {
  Resolve,
  ActivatedRouteSnapshot,
  RouterStateSnapshot,
  Router
} from '@angular/router';
import { Observable, throwError } from 'rxjs';
import { catchError, tap, delay } from 'rxjs/operators';
import { SearchService } from './search.service';
import { HttpErrorResponse } from '@angular/common/http';

@Injectable()
export class VendorResolverService implements Resolve<any> {
  constructor(private searchService: SearchService, private router: Router) {}
  resolve(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<any[]> {
    const id = route.params['id'];
    return this.searchService.getVendorDetails(id).pipe(
      tap(data => data),
      catchError(this.handleError)
    );
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
}
