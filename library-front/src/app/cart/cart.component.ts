import { Component, inject } from '@angular/core';
import { Order } from '../interfaces/entities';
import { ActivatedRoute, NavigationEnd, Router } from '@angular/router';
import { CartService } from '../services/cart.service';
import { filter } from 'rxjs';
import { success, fail } from 'src/utils/general';
import { delay } from 'rxjs';
@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html'
})
export class CartComponent {
  orders: Order[] = [];
  cartService: CartService = inject(CartService);
  constructor(private route: ActivatedRoute, private router: Router) {
    this.getOrderList();
  }

  onCheckboxChange() {
    console.log(this.orders);
  }
  goToHome() {
    this.router.navigate(['home/']);
  }
  async getOrderList() {
    try
    {
      const orders = await this.cartService.getOrders(false);
      this.orders = orders;
    }
    catch(e) {
      console.log('error fetching orders');
    }
  }
  async removeOrder(orderId: number) {
    try
    {
      await this.cartService.removeOrder(orderId);
      window.location.reload();
    }
    catch(e) {
      console.log('error deleting order');
    }
    
  }

  async purchase() {
    try
    {
      for(let order of this.orders)
      {
        if(order.selected)
        {
          await this.cartService.buyOrder(order.id); 
        }
      }
      success('Orders purchased successfully');
      this.router.navigate(['library']);
    }
    catch(e) {
      console.log('error fetching orders');
      fail('Error purchasing');
    }
  }
}
