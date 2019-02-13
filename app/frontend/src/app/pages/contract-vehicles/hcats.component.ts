import { Component, OnInit } from '@angular/core';
import { SearchService } from '../search/search.service';
import { Router } from '@angular/router';

@Component({
  selector: 'discovery-hcats',
  templateUrl: './hcats.component.html',
  styles: [
    `
      .usa-hero {
        background-image: url(/frontend/assets/images/hero-generic-vehicles.jpg);
        color: #fff !important;
      }
    `
  ]
})
export class HcatsComponent implements OnInit {
  pools: any[] = [];
  vehicle = 'HCATS';
  error_message;
  constructor(private searchService: SearchService, private router: Router) {}

  ngOnInit() {
    this.searchService.getPoolsByVehicle(this.vehicle).subscribe(
      data => {
        this.pools = data['results'];
        this.pools.sort(this.searchService.sortByNumberAsc);
      },
      error => (this.error_message = <any>error)
    );
  }

  routeToLink(pool: any, vehicles: string, serviceCategories: string) {	
    serviceCategories = this.searchService.formatServiceCategories(serviceCategories, pool.number);	
    this.router.navigate(['/search'], { queryParams: { vehicles: vehicles, service_categories:serviceCategories }});	
  }
}
