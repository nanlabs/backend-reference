import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { Resource1Module } from './resource1/resource1.module';
import { Resource2Module } from './resource2/resource2.module';

@Module({
  imports: [Resource1Module, Resource2Module],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
