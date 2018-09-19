import { Component, OnInit } from '@angular/core';
import { SearchService } from './search.service';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  templateUrl: './vendor-detail.component.html',
  styleUrls: ['./vendor-detail.component.css']
})
export class VendorDetailComponent implements OnInit {
  error_message;
  vendor: any;
  spinner = true;
  sbd_col = true;
  contract_vehicles;
  service_categories;
  duns: string;
  constructor(
    private searchService: SearchService,
    private router: Router,
    private route: ActivatedRoute
  ) {}
  ngOnInit() {
    this.getContractVehicles();
  }
  getContractVehicles() {
    this.searchService.getContractVehicles().subscribe(
      data => {
        this.contract_vehicles = data['results'];
        this.getServiceCategories();
      },
      error => (this.error_message = <any>error)
    );
  }
  getServiceCategories() {
    this.searchService.getServiceCategories(['All']).subscribe(
      data => {
        this.service_categories = this.buildItems(data['results']);
        this.getVendorDetails();
      },
      error => (this.error_message = <any>error)
    );
  }
  getVendorDetails() {
    const id = this.route.snapshot.params['dun'];
    this.searchService.getVendorDetails(id).subscribe(
      data => {
        this.spinner = false;
        this.vendor = data;
        this.duns = data['duns'];
        this.vendor['pools'] = this.buildPoolsByUniqueContractNumber(data);
      },
      error => (this.error_message = <any>error)
    );
  }
  buildItems(obj: any[]) {
    const categories = [];
    for (const category of obj) {
      const item = {};
      item['id'] = category['id'];
      item['name'] = category['name'];
      item['vehicle_id'] = category['vehicle']['id'];
      item['vehicle'] = category['vehicle']['id'].replace('_', ' ');
      categories.push(item);
    }
    return categories;
  }
  getVehicleDescription(vehicle: string) {
    return this.searchService.getItemDescription(
      this.contract_vehicles,
      vehicle,
      'id',
      'name'
    );
  }
  getServiceCategoryDescription(id: string) {
    return this.searchService.getItemDescription(
      this.service_categories,
      id,
      'id',
      'name'
    );
  }
  getContactInfo(contacts: any[]): string {
    let html = '';
    for (const item of contacts) {
      let name = '';
      let phone = '';
      let email = '';
      if (item.name) {
        name = '<span class="db">' + item.name + '</span>';
      }
      if (item.phones[0].number) {
        phone = '<span class="db">' + item.phones[0].number + '</span>';
      }
      if (item.emails[0].address) {
        email =
          '<span class="db pad-bottom"><a href="mailto:' +
          item.emails[0].address +
          '">' +
          item.emails[0].address +
          '</a></span>';
      }
      html += name + phone + email;
    }
    return html;
  }
  getZones(zones: any[]) {
    let str = '';
    for (const item of zones) {
      str += item.id + ', ';
    }

    return str.slice(0, -2);
  }
  toggleSBD() {
    this.sbd_col = !this.sbd_col;
  }
  buildPoolsByUniqueContractNumber(data: any[]) {
    const contracts: any[] = [];
    for (const item of data['pools']) {
      let pool = {};
      if (!this.searchService.existsIn(contracts, item.piid, 'piid')) {
        pool = item;
        pool['service_categories'] = [];
        pool['setasides'] = this.searchService.commaSeparatedList(
          item.setasides,
          'code'
        );
        pool['zones'] = item.zones.sort(this.searchService.sortByIdAsc);
        contracts.push(pool);
      }
      /** Push service categories to contracts */
      for (const cat of contracts) {
        if (cat['piid'] === item.piid) {
          cat['service_categories'].push(item.pool);
        }
      }
    }

    return contracts;
  }
  returnSetAside(arr: any[], code: string): boolean {
    if (arr.length > 0) {
      return arr.includes(code);
    } else {
      return false;
    }
  }
}
