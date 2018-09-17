import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { SearchComponent } from './search.component';
import { VendorDetailComponent } from './vendor-detail.component';

const routes: Routes = [
  {
    path: 'search',
    component: SearchComponent
  },
  { path: 'vendor/:dun', component: VendorDetailComponent },
  { path: 'vendor', redirectTo: '/search', pathMatch: 'full' }
];
// const routes: Routes = [
//   {
//     path: 'search',
//     component: SearchComponent,
//     children: [
//       { path: '', component: ChooseFiltersComponent },
//       { path: 'contracts/:search', component: ContractsComponent },
//       { path: 'contracts', redirectTo: '/search', pathMatch: 'full' },
//       { path: 'vendors/:search', component: VendorsComponent },
//       { path: 'vendors', redirectTo: '/search', pathMatch: 'full' }
//     ]
//   }
// ];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SearchRoutingModule {}
