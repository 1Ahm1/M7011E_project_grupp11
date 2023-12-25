import { Component, inject } from '@angular/core';
import { Order } from '../interfaces/entities';
import { CartService } from '../services/cart.service';
import { ActivatedRoute, Router, RouterEvent } from '@angular/router';

@Component({
  selector: 'app-library',
  templateUrl: './library.component.html'
})
export class LibraryComponent {
  orders: Order[] = [];
  cartService: CartService = inject(CartService);
  constructor(private router: Router) {
    this.getOrderList();
  }

  goToHome() {
    this.router.navigate(['home/']);
  }
  async getOrderList() {
    try
    {
      const orders = await this.cartService.getOrders(true);
      this.orders = orders;
    }
    catch(e) {
      console.log('error fetching orders');
    }
  }
}
