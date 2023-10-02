import { Controller, Get } from '@nestjs/common';
import { AppService } from './app.service';
import { MessagePattern } from '@nestjs/microservices';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @MessagePattern('get_version')
  getVersion() {
    return '0.0.21';
  }

  @MessagePattern('get_hello')
  getHello() {
    return this.appService.getHello();
  }
}
