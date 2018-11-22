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
      if (document.getElementById('discovery').classList.contains('push')) {
        document.getElementById('discovery').classList.remove('push');
      }
      window.scrollTo(0, 0);
    });
  }
}
