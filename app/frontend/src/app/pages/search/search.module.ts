import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SearchRoutingModule } from './search-routing.module';
import { SearchComponent } from './search.component';
import { FiltersComponent } from './filters.component';
import { ActiveFiltersComponent } from './filters/active-filters.component';
import { FilterContractVehiclesComponent } from './filters/filter-contract-vehicles.component';
import { FilterSbdComponent } from './filters/filter-sbd.component';
import { ChooseFiltersComponent } from './choose-filters.component';
import { FilterKeywordsComponent } from './filters/filter-keywords.component';
import { FormsModule } from '@angular/forms';
import { ModalComponent } from '../../common/modal.component';
import { SpinnerComponent } from '../../common/spinner.component';
import { FilterNaicsComponent } from './filters/filter-naics.component';
import { FilterServiceCategoriesComponent } from './filters/filter-service-categories.component';
import { FilterCertificationsComponent } from './filters/filter-certifications.component';
import { FilterContractPricingTypeComponent } from './filters/filter-contract-pricing-type.component';
import { FilterContractThresholdComponent } from './filters/filter-contract-threshold.component';
import { FilterAgencyPerformanceComponent } from './filters/filter-agency-performance.component';
import { FilterPscComponent } from './filters/filter-psc.component';
import { FilterZoneComponent } from './filters/filter-zone.component';
import { ListComponent } from '../../common/list.component';
import { VendorDetailComponent } from './vendor-detail.component';
import { SearchSpinnerComponent } from './search-spinner.component';
import { TblContractHistoryComponent } from './tbl-contract-history.component';

@NgModule({
  imports: [CommonModule, SearchRoutingModule, FormsModule],
  declarations: [
    SearchComponent,
    ModalComponent,
    FiltersComponent,
    ActiveFiltersComponent,
    ChooseFiltersComponent,
    FilterKeywordsComponent,
    FilterContractVehiclesComponent,
    FilterSbdComponent,
    FilterNaicsComponent,
    FilterServiceCategoriesComponent,
    FilterCertificationsComponent,
    FilterContractPricingTypeComponent,
    FilterContractThresholdComponent,
    FilterAgencyPerformanceComponent,
    FilterPscComponent,
    FilterZoneComponent,
    SpinnerComponent,
    ListComponent,
    VendorDetailComponent,
    SearchSpinnerComponent,
    TblContractHistoryComponent
  ]
})
export class SearchModule {}
