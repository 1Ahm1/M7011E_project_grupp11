import { Component, inject } from '@angular/core';
import { AdminService } from '../services/admin.service';
import { AdminOrder } from '../interfaces/entities';

@Component({
  selector: 'app-admin-home',
  templateUrl: './admin-home.component.html'
})
export class AdminHomeComponent {
  orders: AdminOrder[] = [];
  adminService: AdminService = inject(AdminService);
  constructor() {
    this.getOrderList();
  }
  async getOrderList() {
    try
    {
      const orders = await this.adminService.getOrders();
      this.orders = orders;
    }
    catch(e) {
      console.log('error fetching orders');
    }
  }

  async removeOrder(orderId: number) {
    try
    {
      await this.adminService.removeOrder(orderId);
      window.location.reload();
    }
    catch(e) {
      console.log('error deleting order');
    }
  }
}
