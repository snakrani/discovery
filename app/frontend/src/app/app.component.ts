import { Component } from '@angular/core';
import { Router } from '@angular/router';
declare const document: any;
@Component({
  selector: 'discovery-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  APP_ASSETS = '/frontend/';
  title = 'discovery';
  another: string;

  constructor(private router: Router) {
    router.events.subscribe(() => {
      if (document.getElementById('discovery').style.marginLeft === '310px') {
        document.getElementById('discovery').style.marginLeft = '0px';
      }
    });
  }
}
