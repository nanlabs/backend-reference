import { PartialType } from '@nestjs/mapped-types';
import { CreateResource2Dto } from './create-resource2.dto';

export class UpdateResource2Dto extends PartialType(CreateResource2Dto) {}
